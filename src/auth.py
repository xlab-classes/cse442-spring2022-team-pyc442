from types import NotImplementedType
import bcrypt
from user import User

#Function for authenticating users, returns a User object if correct info is give returns None if invalid
def authenticate(username: str, password: str):
    if(len(username) < 1):
        return None
    #TODO add database parts here
    hashpass = NotImplementedType #need database to use
    if bcrypt.checkpw(bytes(password), hashpass):
        return User(NotImplemented, NotImplemented, NotImplemented, NotImplemented) #Need database to finish here
    return None