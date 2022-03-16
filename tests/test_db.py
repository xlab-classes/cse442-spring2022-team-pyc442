import pytest
from src.database.wireguard_db import add_users, changeBannedStatus, deleteUserByName, general_query, getUserById, modifyUsername, setup_db, create_database, deleteAllTuples, getUserByName
import bcrypt

def test_adding_more_users():
    setup_db()
    create_database()

    add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
    add_users("2", "any2@any2.com", "username2", bcrypt.hashpw(b"password2", bcrypt.gensalt()), 0, 0)
    add_users("3", "any3@any3.com", "username3", bcrypt.hashpw(b"password3", bcrypt.gensalt()), 0, 1)

    #Checks to make sure the info is returned
    retVal = general_query()
    assert retVal != None

#tests for incorrect username on authenticate function
def test_for_user_id():
    #Checks if the user by their id is there
    retVal = getUserById("2")
    assert retVal != None
    #Checks if it's not there
    retVal = getUserById("4")
    assert retVal == None

#tests for empty password on authenticate function
def test_for_user_name():
    retVal = getUserByName("username3")
    assert retVal != None
    retVal = getUserByName("username10")
    assert retVal == None

#tests for empty username on authenticate function
def test_for_modification():
    retVal = modifyUsername("2", "changed_20")
    assert retVal != None
    retVal = modifyUsername("5", "changed_25")
    assert retVal == None

#tests for invalid password on authenticate function
def test_banned_status():
    retVal = changeBannedStatus("2", 0)
    assert retVal != None
    retVal = changeBannedStatus("3", 1)
    assert retVal != None

#tests for empty password and username on authenticate function
def test_delete_user():
    retVal = deleteUserByName("username")
    assert retVal == True
    retVal = deleteUserByName("changed20")
    assert retVal == True
    retVal = deleteUserByName("username3") 
    assert retVal == False