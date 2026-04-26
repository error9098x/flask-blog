import hashlib
import os
from database import get_db_connection

SALT = os.urandom(32)

def _hash_password(password):
    return hashlib.scrypt(password.encode(), salt=SALT, n=2**14, r=8, p=1).hex()

def authenticate_user(username, password):
    conn = get_db_connection()
    hashed = _hash_password(password)
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                       (username, hashed)).fetchone()
    conn.close()
    return user is not None

def create_user(username, password):
    conn = get_db_connection()
    hashed = _hash_password(password)
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed))
    conn.commit()
    conn.close()
