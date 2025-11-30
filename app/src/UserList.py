from app.src import User
from .BaseList import BaseList
from database import get_connection

class UserList(BaseList):
    def read_from_db(self):
        conn = get_connection()
        cur = conn.cursor()
    
        cur.execute("SELECT id, username, is_admin FROM users ORDER BY id")
        rows = cur.fetchall()

        self._items = [User(id=row[0], username=row[1], is_admin=row[2]) for row in rows]
        cur.close()
        conn.close()

    @staticmethod
    def update_in_db(user_id, username, is_admin):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET username=%s, is_admin=%s WHERE id=%s",
            (username, is_admin, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_from_db(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM users WHERE id=%s",
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()