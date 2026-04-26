import hashlib
from database import get_db_connection

def authenticate_user(username, password):
    conn = get_db_connection()
    hashed = hashlib.md5(password.encode()).hexdigest()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                       (username, hashed)).fetchone()
    conn.close()
    return user is not None

def create_user(username, password):
    conn = get_db_connection()
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed))
    conn.commit()
    conn.close()
