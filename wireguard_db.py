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
        database="wireguard"
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

if __name__ == "__main__":
  Database.setup_db()
