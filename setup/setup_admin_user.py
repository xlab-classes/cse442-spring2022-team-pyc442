import bcrypt
import getpass
import sys
import subprocess
import mysql.connector
from mysql.connector import errorcode
import ipaddress


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

def add_user_server(uid, priv, pub, ipadrr):
    cnx = mysql.connector.connect( # connceting to database
      host="localhost",
      user="wireguard",
      password=sys.argv[1],
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
# create private key
privkey = subprocess.run(['wg', 'genkey'], capture_output=True)
# make private key pipeable so that wg pubkey | echo <private key> works as expected
pipe = subprocess.Popen(['echo', privkey.stdout], stdout=subprocess.PIPE)
# create the public key
pubkey = subprocess.run(['wg', 'pubkey'], capture_output=True, stdin=pipe.stdout)
ip = "10.8.0.2"
subprocess.run(['sudo', 'wg-quick', 'up', 'wg0'])
subprocess.run(['sudo', 'wg', 'set', 'wg0', 'peer', pubkey.stdout.decode().strip(), 'allowed-ips', ip])
subprocess.run(['sudo', 'wg-quick', 'down', 'wg0'])
ip = int(ipaddress.ip_address('10.8.0.2'))
add_user_server("1", privkey, pubkey, ip)
