from src import auth
from src.user import User
from src.auth import authenticate

def test_correct_creds():
    retVal = authenticate("username", "password")
    #Checks to make sure User object was returned
    assert type(retVal) == User
    #Checks to make sure username is correct within user object
    assert retVal.get_username == "username"
    #Checks to make sure the is_authenticated property works
    assert retVal.is_authenticated == True
    #Checks to make sure the is_active property is working
    assert retVal.is_active == True

def test_incorrect_creds():
    retVal = authenticate("invalUser", "password")
    assert retVal == None
    retVal = authenticate("username", "")
    assert retVal == None
    retVal = authenticate("", "password")
    assert retVal == None
    retVal = authenticate("username", "invalidPass")
    assert retVal == None