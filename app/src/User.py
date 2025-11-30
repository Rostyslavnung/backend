import psycopg2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_connection

class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password_hash, is_admin FROM users WHERE username = %s",
            (username,)
        )
        row = cur.fetchone()
        conn.close()
        return User(*row) if row else None
    
    def set_password(self, new_password):
        new_hash = generate_password_hash(new_password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (new_hash, self.id)
        )
        conn.commit()
        conn.close()
        self.password_hash = new_hash

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password_hash, is_admin FROM users WHERE id = %s",
            (user_id,)
        )
        row = cur.fetchone()
        conn.close()
        return User(*row) if row else None
        
def load_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, is_admin FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return User(*row)
    return None

def create_user(username, password, is_admin=False):
    password_hash = generate_password_hash(password)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, password_hash, is_admin)
        VALUES (%s, %s, %s) RETURNING id
    """, (username, password_hash, is_admin))

    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return user_id
