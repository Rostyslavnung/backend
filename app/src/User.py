from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.id = id
        self.name = name
        self.active = active

    def get_id(self):
        return self.id
    
    @classmethod
    def get(cls, user_id):
        # Імітація бази користувачів (у реальному проєкті — БД)
        if user_id == "1":
            return cls(name="testuser", id="1")
        return None

    @classmethod
    def get_by_username(cls, username):
        if username == "testuser":
            return cls(name="testuser", id="1")
        return None
    def check_password(self, password):
        # This should check the password against your user data source
        return password == "testpass"
    
    @property
    def is_active(self):
        return self.active