from json.tool import main
import pylint
import mysql.connector
from mysql.connector import errorcode
import bcrypt

#Sets up the database
def setup_db():
  mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FalaWB@321",
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
      
  cnx = mysql.connector.connect(
      host="localhost",
      user="root",
      password="FalaWB@321")

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
    
#Adds users to the server
def add_users(id, email, username, password, is_admin, is_banned):
      cnx = mysql.connector.connect( # connceting to database
      host="localhost",
      user="root",
      password="FalaWB@321",
      database="wireguard"
      )

      cursor = cnx.cursor()

      add_user = ("INSERT INTO wireguard "
                "(user_id, email, username, password, admin, banned) "
                "VALUES (%s, %s, %s, %s, %s, %s)") # query to add user

      data_user = (id, email, username, password, is_admin, is_banned)

      cursor.execute(add_user, data_user)

      cnx.commit()

      cursor.close()
      cnx.close()

    #Execute the general query
def general_query():
      cnx = mysql.connector.connect( 
      host="localhost",
      user="root",
      password="FalaWB@321",
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
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = [] #initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("SELECT * FROM wireguard WHERE user_id = %s") #writing query to find user by uid

      user_id = uid

      cursor.execute(query, (user_id,))

      for (user_id, email, username, password, admin, banned) in cursor: # for loop to poulate user_data
        user_data.append([user_id, email, username, password, admin, banned])

      cursor.close()
      cnx.close()

      if user_data == []:
        return None
      return user_data[0] #returning first element of user_data

#Gets a user entry by username, returns user data as first element of list user_data
def getUserByName(uname):
      cnx = mysql.connector.connect( #connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = [] #initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("SELECT * FROM wireguard WHERE username = %s") #writing query to find a user by username

      cursor.execute(query, (uname,))

      for (user_id, email, username, password, admin, banned) in cursor: # for loop to poulate user_data
        user_data.append([user_id, email, username, password, admin, banned])

      cursor.close()
      cnx.close()
      if user_data == []:
        return None
      return user_data[0] #returning first element of user_data

#change a user's username to newUname, returns user data as first element of list user_data
def modifyUsername(uid, newUname):
      cnx = mysql.connector.connect( # connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = [] # initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("UPDATE wireguard SET username = %s WHERE user_id = %s") #writing query to update username

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
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )
      user_data = [] # initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("UPDATE wireguard SET banned = %s WHERE user_id = %s") #writing query to update ban status

      cursor.execute(query, (newBanStatus, uid))

      cnx.commit()

      query = ("SELECT * FROM wireguard WHERE user_id = %s") #write query to get user data

      cursor.execute(query, (uid,))

      for (user_id, email, username, password, admin, banned) in cursor: #for loop to populate user_data
        user_data.append([user_id, email, username, password, admin, banned])

      cursor.close()
      cnx.close()

      if user_data == []:
        return None
      return user_data[0] #returning first element of user_data

def deleteUserByName(name):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

    user_data = []

    cursor = cnx.cursor()

    query2 = ("SELECT * FROM wireguard WHERE EXISTS (SELECT * FROM wireguard WHERE username = %s)")

    cursor.execute(query2, (name,))

    for (user_id, email, username, password, admin, banned) in cursor: #for loop to populate user_data
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
    





#currently deletes all entries from the database, change to only delete a specified tuple from the database
def deleteAllTuples():
      cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      cursor = cnx.cursor()

      query = ("DELETE FROM wireguard")

      cursor.execute(query)

      cnx.commit()

      cursor.close()
      cnx.close()


#testing
if __name__ == "__main__":
  add_users("1", "any@any.com", "username", bcrypt.hashpw(b"password", bcrypt.gensalt()), 1, 0)
  add_users("2", "any2@any2.com", "changed_20", bcrypt.hashpw(b"password2", bcrypt.gensalt()), 0, 1)
  add_users("3", "any3@any3.com", "username3", bcrypt.hashpw(b"password3", bcrypt.gensalt()), 0, 0)
  print(deleteUserByName("username"))
  print(deleteUserByName("changed_20"))
  print(deleteUserByName("username3"))