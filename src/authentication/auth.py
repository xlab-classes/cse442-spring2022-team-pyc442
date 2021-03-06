import bcrypt
from src.authentication.user import User
from src.database.wireguard_db import getUserByName

#Function for authenticating users, returns a User object if correct info is give returns None if invalid
# @param1 username stores the username of the user to authenticate (will be used to get info from database)
# @param2 password store the password to be hashed and checked
def authenticate(username: str, password: str):
    if(username == None or password == None):
        return None
    if(len(username) < 1):
        return None
    # gets user info in a list order of (user_id, email, username, password, admin, banned)
    userInfo = getUserByName(username)
    if (userInfo == None or userInfo == []):
        return None
    hashpass = userInfo[3] #need database to use
    #checks if password is correct
    if bcrypt.checkpw(bytes(password, "UTF-8"), bytes(hashpass, "UTF-8")):
        #if password is correct return a user object
        # order of User init is (username: str, userid: str, isAdmin: bool, isBanned: bool)
        return User(userInfo[2], userInfo[0], userInfo[4], userInfo[5]) #Need database to finish here
    #if password is incorrect return none
    return None

if __name__ == "__main__":
    #("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0
    id = "1"
    email = "any@any.com"
    name = "username"
    password = bcrypt.hashpw(b"password", bcrypt.gensalt())
    admin = 1
    banned = 0

    authenticate(name, password)