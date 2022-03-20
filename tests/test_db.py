import bcrypt
import src.database.wireguard_db as db

def test_adding_more_users():
    db.deleteAllTuples()
    db.setup_db()
    db.create_database()

    db.add_users("1", "any@any.com", "username", bcrypt.hashpw(b"pwd", bcrypt.gensalt()), 1, 0)
    db.add_users("2", "any2@any.com", "username2", bcrypt.hashpw(b"pwd2", bcrypt.gensalt()), 0, 0)
    db.add_users("3", "any3@any.com", "username3", bcrypt.hashpw(b"pwd3", bcrypt.gensalt()), 0, 1)

    #Checks to make sure the info is returned
    test1 = db.general_query()
    assert test1 is not None

#tests for incorrect username on authenticate function
def test_for_user_id():
    #Checks if the user by their id is there
    test2 = db.getUserById("2")
    assert test2 is not None
    #Checks if it's not there
    test3 = db.getUserById("4")
    assert test3 is None

#tests for empty password on authenticate function
def test_for_user_name():
    test4 = db.getUserByName("username3")
    assert test4 is not None
    test5 = db.getUserByName("username10")
    assert test5 is None

#tests for empty username on authenticate function
def test_for_modification():
    test6 = db.modifyUsername("2", "changed_20")
    assert test6 is not None
    test7 = db.modifyUsername("5", "changed_25")
    assert test7 is None

#tests for invalid password on authenticate function
def test_banned_status():
    test8 = db.changeBannedStatus("2", 1)
    assert test8 is not None
    test9 = db.changeBannedStatus("3", 0)
    assert test9 is not None

#tests for empty password and username on authenticate function
def test_delete_user():
    test10 = db.deleteUserByName("username")
    assert test10 is True
    test11 = db.deleteUserByName("changed_20")
    assert test11 is True
    test12 = db.deleteUserByName("username3")
    assert test12 is True
    test13 = db.deleteUserByName("username3")
    assert test13 is False