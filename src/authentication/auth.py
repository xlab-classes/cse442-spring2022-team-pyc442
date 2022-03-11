import bcrypt
from src.authentication.user import User

#Function for authenticating users, returns a User object if correct info is give returns None if invalid
def authenticate(username: str, password: str) -> User:
    if(len(username) < 1):
        return None
    #TODO add database parts here
    hashpass = NotImplemented #need database to use
    if bcrypt.checkpw(bytes(password.encode("UTF-8"), "UTF-8"), bytes(hashpass, "UTF-8")):
        return User(NotImplemented, NotImplemented, NotImplemented, NotImplemented) #Need database to finish here
    return None