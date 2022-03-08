from json.tool import main
import os
import mysql.connector

class Database:
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

  #Adds users to the server
  def addUsers(username, hashpass, userid, admin):
    userid = os.random(16) #ID will be randomized
    name = username
    password = hashpass
    is_admin = admin

  def create_database(self):
    DB_NAME = 'wireguard'
    TABLES = {}
    TABLES['wireguard'] = (
      "Create Table Wireguard ("
      "user_id  varchar(9),"
      "email   varchar(32),"
      "username     varchar(32),"
      "password  varchar(64),"
      "admin      bool,"
      "banned   bool,"
      "PRIMARY KEY (user_id)"
      ") ENGINE=InnoDB")
    
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FalaWB@321",
    )

    cursor = cnx.cursor()
    try:
          cursor.execute(
              "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
      print("Database {} does not exists.".format(DB_NAME))
      if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        self.create_database()
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
      else:
        print(err)
        exit(1)


if __name__ == "__main__":
  Database.setup_db()
  Database.create_database(Database)
