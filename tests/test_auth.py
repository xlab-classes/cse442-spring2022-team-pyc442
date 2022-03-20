import pytest
from src.authentication.user import User
from src.authentication.auth import authenticate
from src.database.wireguard_db import add_users, deleteUserByName, setup_db, create_database, deleteAllTuples
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
    setup_db()
    create_database()

    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "password")
    deleteAllTuples()
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
    deleteAllTuples()
    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("invalUser", "password")
    deleteAllTuples()
    assert retVal == None

#tests for empty password on authenticate function
def test_empty_pass():
    deleteAllTuples()
    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "")
    deleteAllTuples()
    assert retVal == None

#tests for empty username on authenticate function
def test_empty_username():
    deleteAllTuples()
    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("", "password")
    deleteAllTuples()
    assert retVal == None

#tests for invalid password on authenticate function
def test_invalid_password():
    deleteAllTuples()
    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("username", "invalidPass")
    deleteAllTuples()
    assert retVal == None

#tests for empty password and username on authenticate function
def test_empty_creds():
    deleteAllTuples()
    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    retVal = authenticate("","")
    deleteAllTuples()
    assert retVal == None