from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin=False, active=True):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.active = active

    def get_id(self):
        return str(self.id)

    @classmethod
    def get(cls, user_id):
        # ТУТ має бути завантаження з бази або файла
        # Для прикладу — фіксований користувач
        if str(user_id) == "1":
            return cls(
                id="1",
                username="admin",
                password_hash="testpass",
                is_admin=True  # ← адмін!
            )
        if str(user_id) == "2":
            return cls(
                id="2",
                username="user",
                password_hash="userpass",
                is_admin=False
            )
        return None

    @classmethod
    def get_by_username(cls, username):
        # Імітація бази (можеш замінити на CSV або DB)
        if username == "admin":
            return cls(
                id="1",
                username="admin",
                password_hash="testpass",
                is_admin=True
            )
        if username == "user":
            return cls(
                id="2",
                username="user",
                password_hash="userpass",
                is_admin=False
            )
        return None

    def check_password(self, password):
        return password == self.password_hash

    @property
    def is_active(self):
        return self.active
