import mysql.connector
from mysql.connector import errorcode
import json

DB_HOST = "localhost"
DB_USERNAME="root"
DB_PASSWORD="password"

def setup_con_db(debug=False):
    if not debug:
        global DB_USERNAME
        global DB_PASSWORD
        with open("/var/www/wireguard/database.cfg", "r") as f:
            config = json.load(f)
            DB_USERNAME = config["username"]
            DB_PASSWORD = config["password"]


#Sets up the database
def setup_db():
    mydb = mysql.connector.connect(
          host=DB_HOST,
          user=DB_USERNAME,
          password=DB_PASSWORD
          )

    if mydb:
        print("connected")
    else:
        print("failed")

    mydb.close()

#Creates the database
def create_database():
    DB_NAME = 'wireguard'
    TABLES = {}
    TABLES['wireguard'] = (
      "CREATE TABLE `wireguard` ("
      "   `user_id`  varchar(9) NOT NULL,"
      "   `email`   varchar(32) NOT NULL,"
      "   `username`     varchar(32) NOT NULL,"
      "   `password`  varchar(64) NOT NULL,"
      "   `admin`      tinyint(1),"
      "   `banned`   tinyint(1),"
      "   PRIMARY KEY (`user_id`)"
      ") ENGINE=InnoDB")
    TABLES['server'] = (
      "CREATE TABLE `server` ("
      "   `uid` varchar(9) NOT NULL,"
      "   `private_key` varchar(256) NOT NULL,"
      "   `public_key` varchar(256) NOT NULL,"
      "   `ip` int(32),"
      "   PRIMARY KEY (`uid`),"
      "   CONSTRAINT `server_id` FOREIGN KEY (`uid`)"
      "        REFERENCES `wireguard` (`user_id`) ON DELETE CASCADE"
      ") ENGINE=InnoDB")
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD)

    cursor = cnx.cursor()

    #checks if database is created
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
            print("Database {} created successfully.".format(DB_NAME))

      #checks if the table is existed
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()

#need to create table for server info

#Adds users to the server
def add_users(uid, email, username, password, is_admin, is_banned):
    cnx = mysql.connector.connect( # connceting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
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

    #Execute the general query
def general_query():
    cnx = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
      )

    user_data = []

    cursor = cnx.cursor()

    query = ("SELECT * FROM wireguard") 

    cursor.execute(query)

    for (user_id, email, username, password, admin, banned) in cursor:
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()
    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data

#Gets a user entry by user id, returns user data as first element of list user_data
def getUserById(uid):
    cnx = mysql.connector.connect( #connecting to database
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="wireguard"
      )

    user_data = [] #initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("SELECT * FROM wireguard WHERE user_id = %s") #writing query to find user by uid

    user_id = uid

    cursor.execute(query, (user_id,))

    for (user_id, email, username, password, admin, banned) in cursor: # to populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()

    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data

#Gets a user entry by username, returns user data as first element of list user_data
def getUserByName(uname):
    cnx = mysql.connector.connect( #connecting to database
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="wireguard"
      )

    user_data = [] #initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("SELECT * FROM wireguard WHERE username = %s") #find a user by username

    cursor.execute(query, (uname,))

    for (user_id, email, username, password, admin, banned) in cursor: #populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()
    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data

#change a user's username to newUname, returns user data as first element of list user_data
def modifyUsername(uid, newUname):
    cnx = mysql.connector.connect( # connecting to database
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="wireguard"
      )

    user_data = [] # initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("UPDATE wireguard SET username = %s WHERE user_id = %s") #to update username

    cursor.execute(query, (newUname, uid))

    cnx.commit()

    query = ("SELECT * FROM wireguard WHERE user_id = %s") #write query to get user data

    cursor.execute(query, (uid,))

    for user_id, email, username, password, admin, banned in cursor: #for loop to populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()
    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data # returning first element of user_data

#change a user's ban status, returns user data as first element of list user_data
def changeBannedStatus(uid, newBanStatus):
    cnx = mysql.connector.connect( # connecting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )
    user_data = [] # initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("UPDATE wireguard SET banned = %s WHERE user_id = %s") #to update ban status

    cursor.execute(query, (newBanStatus, uid))

    cnx.commit()

    query = ("SELECT * FROM wireguard WHERE user_id = %s") #write query to get user data

    cursor.execute(query, (uid,))

    for (user_id, email, username, password, admin, banned) in cursor: #populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()

    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data

def changePassword(uname, newp):
    cnx = mysql.connector.connect( # connecting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )
    user_data = [] # initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("UPDATE wireguard SET password = %s WHERE username = %s") #to update ban status

    cursor.execute(query, (newp, uname))

    cnx.commit()

    query = ("SELECT * FROM wireguard WHERE username = %s") #write query to get user data

    cursor.execute(query, (uname,))

    for (user_id, email, username, password, admin, banned) in cursor: #populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

    cursor.close()
    cnx.close()

    if user_data == []:
        return None
    return user_data[0] #returning first element of user_data

def deleteUserByName(name):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="wireguard"
      )

    user_data = []

    cursor = cnx.cursor()

    query2 = ("SELECT * FROM wireguard WHERE EXISTS (SELECT * FROM wireguard WHERE username = %s)")

    cursor.execute(query2, (name,))

    for (user_id, email, username, password, admin, banned) in cursor: #populate user_data
        user_data.append((user_id, email, username, password, admin, banned))

    if user_data == []:
        cursor.close()
        cnx.close()
        return False

    query1 = ("DELETE FROM wireguard WHERE username = %s")

    cursor.execute(query1, (name,))

    cnx.commit()


    cursor.close()
    cnx.close()

    return True

def add_user_server(uid, priv, pub, ipadrr):
    cnx = mysql.connector.connect( # connceting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
      )

    cursor = cnx.cursor()

    add_user = ("INSERT INTO server "
                "(uid, private_key, public_key, ip) "
                "VALUES (%s, %s, %s, %s)") # query to add user

    data_user = (uid, priv, pub, ipadrr)

    cursor.execute(add_user, data_user)

    cnx.commit()

    cursor.close()
    cnx.close()

    return True

def get_max_ip():
    cnx = mysql.connector.connect( # connecting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )
    user_data = [] # initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("SELECT max(ip) FROM server") #find a user by username

    cursor.execute(query,)

    for (ip) in cursor: #populate user_data
        user_data.append(ip)

    cursor.close()
    cnx.close()

    if user_data == []:
        return None
    return user_data[0][0] 

def get_user_server(uid):
    cnx = mysql.connector.connect( # connecting to database
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )
    user_data = [] # initializing list, first element will be returned

    cursor = cnx.cursor()

    query = ("SELECT * FROM server WHERE uid = %s") #find a user by username

    cursor.execute(query, (uid,))

    for (uid, private_key, public_key, ip) in cursor: #populate user_data
        user_data.append([uid, private_key, public_key, ip])

    cursor.close()
    cnx.close()

    if user_data == []:
        return None
    return user_data[0] 

#deletes all entries from the database
def deleteAllTuples():
    cnx = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )

    cursor = cnx.cursor()

    query = ("DELETE FROM wireguard")

    cursor.execute(query)

    query2 = ("DELETE FROM server")

    cursor.execute(query2)

    cnx.commit()

    cursor.close()
    cnx.close()

def listBlockedUsers():
    cnx = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database="wireguard"
    )

    banned_users = []

    cursor = cnx.cursor()

    query = ("SELECT username FROM wireguard WHERE banned = 1")

    cursor.execute(query)

    for username in cursor: #populate user_data
        banned_users.append(username[0])

    
    cnx.commit()

    cursor.close()
    cnx.close()

    return banned_users

