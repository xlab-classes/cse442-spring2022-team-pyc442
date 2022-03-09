from json.tool import main
import os
import mysql.connector
from mysql.connector import errorcode
import uuid

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
        password="FalaWB@321",
    )
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
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="FalaWB@321",
    database="wireguard"
    )

    cursor = cnx.cursor()

    add_user = ("INSERT INTO wireguard "
               "(user_id, email, username, password, admin, banned) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

    data_user = (id, email, username, password, is_admin, is_banned)

    cursor.execute(add_user, data_user)

    cnx.commit()

    cursor.close()
    cnx.close()

  def queries():
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="FalaWB@321",
    database="wireguard"
    )

    cursor = cnx.cursor()

    query = ("SELECT * FROM wireguard")

    cursor.execute(query)

    for (user_id, email, username, password, admin, banned) in cursor:
      print("{}, {}, {}, {}, {}, {}".format(user_id, email, username, password, admin, banned))

    cnx.commit()

    cursor.close()
    cnx.close()


if __name__ == "__main__":
  id = str(uuid.uuid4().fields[-1])[:9]
  email = " "
  name = " "
  password = " "
  admin = 0
  banned = 0

  Database.setup_db()
  Database.create_database()
  Database.add_users(id, email, name, password, admin, banned)
  Database.queries()