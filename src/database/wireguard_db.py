from json.tool import main
import os
import mysql.connector
from mysql.connector import errorcode
import uuid

#Sets up the database
def setup_db(self):
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
def create_database(self):
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

      cursor.execute("USE {}".format(DB_NAME))

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
def queries(self):
      cnx = mysql.connector.connect( 
      host="localhost",
      user="root",
      password="FalaWB@321",
      database="wireguard"
      )

      user_data = list(tuple)

      cursor = cnx.cursor()

      query = ("SELECT * FROM wireguard") 

      cursor.execute(query)

      for (user_id, email, username, password, admin, banned) in cursor:
        user_data.append((user_id, email, username, password, admin, banned))

      cnx.commit()

      cursor.close()
      cnx.close()

      return user_data[0]

#Gets a user entry by user id, returns user data as first element of list user_data
def getUserById(self, uid):
      cnx = mysql.connector.connect( #connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = list(tuple) #initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("SELECT * FROM wireguard WHERE user_id = %s") #writing query to find user by uid

      user_id = uid

      cursor.execute(query, (user_id,))

      for (user_id, email, username, password, admin, banned) in cursor: # for loop to poulate user_data
        user_data.append((user_id, email, username, password, admin, banned))


      cnx.commit()

      cursor.close()
      cnx.close()

      return user_data[0] #returning first element of user_data

#Gets a user entry by username, returns user data as first element of list user_data
def getUserByName(self, uname):
      cnx = mysql.connector.connect( #connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = list(tuple) #initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("SELECT * FROM wireguard WHERE username = %s") #writing query to find a user by username

      cursor.execute(query, (uname,))

      for (user_id, email, username, password, admin, banned) in cursor: #for loop to populate user_data
        user_data.append((user_id, email, username, password, admin, banned))

      cnx.commit()

      cursor.close()
      cnx.close()
      return user_data[0] #returning first element of user_data

"""
#change a user's username to newUname, returns user data as first element of list user_data
def modifyUsername(self, uid, newUname):
      cnx = mysql.connector.connect( # connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )

      user_data = list(tuple) # initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("UPDATE wireguard SET username = %s WHERE uid = %s") #writing query to update username

      cursor.execute(query, (newUname, uid))

      query = ("SELECT * FROM wireguard WHERE uid = %s") #write query to get user data

      cursor.execute(query, (uid,))

      for (user_id, email, username, password, admin, banned) in cursor: #for loop to populate user_data
        user_data.append((user_id, email, username, password, admin, banned))

      cnx.commit()

      cursor.close()
      cnx.close()
      return user_data[0] # returning first element of user_data 

#change a user's ban status, returns user data as first element of list user_data
def changeBannedStatus(self, uid, newBanStatus)
      cnx = mysql.connector.connect( # connecting to database
        host="localhost",
        user="root",
        password="FalaWB@321",
        database="wireguard"
      )
      user_data = list(tuple) # initializing list, first element will be returned

      cursor = cnx.cursor()

      query = ("UPDATE wireguard SET banned = %i WHERE uid = %s") #writing query to update ban status

      cursor.execute(query, (newBanStatus, uid))

      query = ("SELECT * FROM wireguard WHERE uid = %s") #write query to get user data

      cursor.execute(query, (uid,))

      for (user_id, email, username, password, admin, banned) in cursor: #for loop to populate user_data
        user_data.append((user_id, email, username, password, admin, banned))

      cnx.commit()

      cursor.close()
      cnx.close()
      return user_data[0] # returning first element of user_data

"""

#currently deletes all entries from the database, change to only delete a specified tuple from the database
def deleteTuple():
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
""" if __name__ == "__main__":
    id = str(uuid.uuid4().fields[-1])[:9]
    email = "test@email.com"
    name = "test_442"
    password = "abc123"
    admin = 1
    banned = 0

    setup_db()
    create_database()
    add_users(id, email, name, password, admin, banned)
    queries()
    getUserById(id)
    getUserByName(name)
    modifyUsername(id, "new_username_442")
    changeBannedStatus(id, 1)
    deleteTuple() """