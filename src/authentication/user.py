from flask_login import UserMixin


# User class used to store the information
class User(UserMixin):

    def __init__(self, username: str, userid: str, isAdmin: bool, isBanned: bool):
        self.username = username
        self.userid = userid
        self.isAdmin = isAdmin
        self.isBanned = isBanned

    def is_active(self) -> bool:
        return self.isBanned

    def get_id(self) -> str:
        return self.userid

    def is_authenticated(self) -> bool:
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.isAdmin

    def get_username(self):
        return self.username
