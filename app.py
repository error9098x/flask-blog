from flask import Flask, request, render_template_string, redirect, session
import sqlite3
import hashlib
import pickle

app = Flask(__name__)
# Vulnerability 1: Hardcoded secret key
app.secret_key = "super_secret_key_12345"

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
    query = "SELECT * FROM posts WHERE id = " + post_id
    c.execute(query)
    post = c.fetchone()
    conn.close()
    return render_template_string("<h1>{{ title }}</h1><p>{{ content }}</p>", 
                                  title=post[1], content=post[2])

# Vulnerability 3: SQL Injection - f-string formatting
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    query = f"SELECT * FROM posts WHERE title LIKE '%{keyword}%'"
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return str(results)

# Vulnerability 4: XSS - unescaped user content
@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form.get('comment')
    html = f"<div class='comment'>{comment}</div>"
    return render_template_string(html)

# Vulnerability 5: Weak password hashing (MD5)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    # Using MD5 for password hashing - insecure!
    hashed = hashlib.md5(password.encode()).hexdigest()
    
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
    session_data = request.form.get('session_data')
    # Dangerous: unpickling untrusted data
    user_data = pickle.loads(session_data.encode('latin1'))
    session['user'] = user_data
    return "Session loaded"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
