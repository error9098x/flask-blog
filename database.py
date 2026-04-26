import sqlite3

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_post(title, content, author):
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                 (title, content, author))
    conn.commit()
    conn.close()

def get_all_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts
