from src.authentication.user import User
from src.authentication.auth import authenticate

def test_correct_creds():
    retVal = authenticate("username", "password")
    #Checks to make sure User object was returned
    assert retVal != None
    #Checks to make sure username is correct within user object
    assert retVal.get_username == "username"
    #Checks to make sure the is_authenticated property works
    assert retVal.is_authenticated == True
    #Checks to make sure the is_active property is working
    assert retVal.is_active == True

#tests for incorrect username on authenticate function
def test_incorrect_username():
    retVal = authenticate("invalUser", "password")
    assert retVal == None

#tests for empty password on authenticate function
def test_empty_pass():
    retVal = authenticate("username", "")
    assert retVal == None

#tests for empty username on authenticate function
def test_empty_username():
    retVal = authenticate("", "password")
    assert retVal == None

#tests for invalid password on authenticate function
def test_invalid_password():
    retVal = authenticate("username", "invalidPass")
    assert retVal == None

#tests for empty password and username on authenticate function
def test_empty_creds():
    retVal = authenticate("","")
    assert retVal == None
