from src.authentication.user import User
from src.authentication.auth import authenticate
import src.database.wireguard_db as db
import bcrypt

#setup database and resets database for tests
#@pytest.fixture()
#def dbsetup():
    #sets up database
    #add in correct user
    #pause until test case is finished
    #yield
    #remove user from database
    #deleteUserByName("username")




def test_correct_creds():
    db.setup_db()
    db.create_database()

    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "password")
    db.deleteAllTuples()
    #Checks to make sure User object was returned
    assert retVal != None
    #Checks to make sure username is correct within user object
    assert retVal.get_username() == "username"
    #Checks to make sure the is_authenticated property works
    assert retVal.is_authenticated() == True
    #Checks to make sure the is_active property is working
    assert retVal.is_active() == False

#tests for incorrect username on authenticate function
def test_incorrect_username():
    db.deleteAllTuples()
    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("invalUser", "password")
    db.deleteAllTuples()
    assert retVal == None

#tests for empty password on authenticate function
def test_empty_pass():
    db.deleteAllTuples()
    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "")
    db.deleteAllTuples()
    assert retVal == None

#tests for empty username on authenticate function
def test_empty_username():
    db.deleteAllTuples()
    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("", "password")
    db.deleteAllTuples()
    assert retVal == None

#tests for invalid password on authenticate function
def test_invalid_password():
    db.deleteAllTuples()
    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "invalidPass")
    db.deleteAllTuples()
    assert retVal == None

#tests for empty password and username on authenticate function
def test_empty_creds():
    db.deleteAllTuples()
    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("","")
    db.deleteAllTuples()
    assert retVal == None
