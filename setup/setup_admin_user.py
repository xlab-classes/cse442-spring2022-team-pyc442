import bcrypt
import getpass
import sys

def add_users(uid, email, username, password, is_admin, is_banned):
    cnx = mysql.connector.connect( # connceting to database
      host="localhost",
      user="wireguard",
      password=sys.argv[1],
      database="wireguard"
      )

    cursor = cnx.cursor()

    add_user = ("INSERT INTO wireguard "
                "(user_id, email, username, password, admin, banned) "
                "VALUES (%s, %s, %s, %s, %s, %s)") # query to add user

    data_user = (uid, email, username, password, is_admin, is_banned)

    cursor.execute(add_user, data_user)

    cnx.commit()

    cursor.close()
    cnx.close()

username = "admin"
password = None
email = None

while (password == None):
        password = getpass.getpass(prompt="Please input the admin user password: ", stream=None)
        if(password == ""):
            print("Invalid password")
            password = None

email = input("Please input the email address of the admin user: ")

add_users("1", email, username, bcrypt.hashpw(bytes(password), bcrypt.gensalt()), True, False)
