from flask import Flask, request, render_template_string, redirect, session
import sqlite3
import hashlib
import json
import os

app = Flask(__name__)
# Fix: Use environment variable for secret key
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key_change_me')

# Database setup
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Vulnerability 2: SQL Injection - string concatenation
@app.route('/post/<post_id>')
def view_post(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    query = "SELECT * FROM posts WHERE id = ?"
    c.execute(query, (post_id,))
    post = c.fetchone()
    conn.close()
    if post is None:
        return "Post not found", 404
    return render_template_string("<h1>{{ title }}</h1><p>{{ content }}</p>", 
                                  title=post[1], content=post[2])

# Vulnerability 3: SQL Injection - f-string formatting
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    query = "SELECT * FROM posts WHERE title LIKE ?"
    c.execute(query, ('%' + keyword + '%',))
    results = c.fetchall()
    conn.close()
    return str(results)

# Vulnerability 4: XSS - unescaped user content
@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form.get('comment', '')
    # Use render_template_string with autoescaping instead of raw HTML concatenation
    return render_template_string("<div class='comment'>{{ comment }}</div>", comment=comment)

# Vulnerability 5: Weak password hashing (MD5)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    # Fix: Use scrypt for secure password hashing
    hashed = hashlib.scrypt(password.encode(), salt=os.urandom(32), n=2**14, r=8, p=1).hex()
    
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
              (username, hashed))
    conn.commit()
    conn.close()
    return redirect('/')

# Vulnerability 6: Insecure deserialization
@app.route('/load_session', methods=['POST'])
def load_session():
    session_data = request.form.get('session_data', '{}')
    # Fix: Use JSON instead of pickle for safe deserialization
    try:
        user_data = json.loads(session_data)
        session['user'] = user_data
        return "Session loaded"
    except json.JSONDecodeError:
        return "Invalid session data", 400

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
