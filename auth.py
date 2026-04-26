import hashlib
import os
from database import get_db_connection

def authenticate_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?',
                       (username,)).fetchone()
    conn.close()
    if user is None:
        return False
    stored_hash = user['password']
    salt, hash_value = stored_hash.split('$', 1)
    computed = hashlib.scrypt(password.encode(), salt=salt.encode(), n=2**14, r=8, p=1, dklen=64).hex()
    return computed == hash_value

def create_user(username, password):
    conn = get_db_connection()
    salt = os.urandom(16).hex()
    hashed = hashlib.scrypt(password.encode(), salt=salt.encode(), n=2**14, r=8, p=1, dklen=64).hex()
    stored = f"{salt}${hashed}"
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                (username, stored))
    conn.commit()
    conn.close()
