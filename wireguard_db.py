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
        Database="wireguard"
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

  def create_database():
    TABLES = {}
    TABLES['wireguard'] = (
      "Create Table Users ("
      "user_id  varchar(9),"
      "email   varchar(32),"
      "username     varchar(32),"
      "password  varchar(64),"
      "admin      bool,"
      "banned   bool,"
      "PRIMARY KEY (user_id)"
      ")ENGINE=InnoDB")
    
    

if __name__ == "__main__":
  Database.setup_db()
