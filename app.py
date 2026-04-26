from flask import Flask, request, render_template_string, redirect, session
import sqlite3
import hashlib
import json
import os

app = Flask(__name__)
# Fixed: Use environment variable for secret key
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

# Fixed: Use parameterized query
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

# Fixed: Use parameterized query with proper LIKE pattern
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

# Fixed: Use render_template_string with autoescaping instead of raw HTML
@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form.get('comment')
    return render_template_string("<div class='comment'>{{ comment }}</div>", comment=comment)

# Fixed: Use scrypt for secure password hashing
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    # Using scrypt for secure password hashing
    hashed = hashlib.scrypt(password.encode(), salt=os.urandom(32), n=2**14, r=8, p=1).hex()
    
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
              (username, hashed))
    conn.commit()
    conn.close()
    return redirect('/')

# Fixed: Use JSON instead of pickle for safe deserialization
@app.route('/load_session', methods=['POST'])
def load_session():
    session_data = request.form.get('session_data')
    # Safe: using JSON instead of pickle
    user_data = json.loads(session_data)
    session['user'] = user_data
    return "Session loaded"

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
