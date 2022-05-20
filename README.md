# cse442-spring2022-team-pyc442  

Pyc442  
Anthony Schiano  
Howie Lin  
Michael Traynor  
Brian Chen  
Michael Lanurias  

# Warning does not work on school server, we deployed to an ubuntu 20.04 digital ocean droplet 

------
# To Test:
Notes: these are only tested on ubuntu 20.04 and in this testing mode you will not be able to run a wireguard server  
1. Install basic dependincies and set them up. Please note you will have to run these are root  
  `sudo apt install python3 python-is-python3 python3-virtualenv mysql-server wireguard-tools`  
  
  You will also need to add in a new user to mysql, in this case please run:  
  `sudo mysql -u root -e "CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';"` 
  where username is the desired username and password is the desired password  
  the give the user permissions where username is the username used in the previous step:  
  `sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS wireguard DEFAULT CHARACTER SET 'utf8';"`  
  `sudo mysql -u root -e "mysql -u root -e "GRANT SELECT, INSERT, UPDATE, DELETE ON wireguard.* TO 'username'@'localhost';"`  
  `mysql -u root -e "FLUSH PRIVILEGES;"`  
  Then create all the tables for the database  
  `mysql -u root -e "USE wireguard; CREATE TABLE IF NOT EXISTS wireguard (
    user_id varchar(9) NOT NULL,
    email varchar(32) NOT NULL,
    username varchar(32) NOT NULL,
    password varchar(64) NOT NULL,
    admin tinyint(1),
    banned tinyint(1),
    PRIMARY KEY (user_id)
) ENGINE=InnoDB; CREATE TABLE IF NOT EXISTS server (
   uid varchar(9) NOT NULL,
   private_key varchar(256) NOT NULL,
    public_key varchar(256) NOT NULL,
    ip int(32),
    PRIMARY KEY (uid),
    CONSTRAINT server_id FOREIGN KEY (uid)
    REFERENCES wireguard (user_id) ON DELETE CASCADE
) ENGINE=InnoDB;"`  
2. clone the git repo (note you may need to install git)  
`git clone git@github.com:xlab-classes/cse442-spring2022-team-pyc442.git`  
then please change directory into the directory created by the above command  
3. to run code use the command Create a virtual environment for python to run and source it  
  `virtualenv venv`  
  `source venv/bin/activate`  
3. Then install the rest of the dependincies  
`pip install -r requirements.txt`  
4. You should then edit the database file to add in your credentials for the database created above  
assuming you are in the root directory of the project  
`nano src/database/wireguard_db.py`  
then change the line for DB_USERNAME and DB_PASSWORD to the correct username and password  

5. You can then either run the server entirly or run the unit testing using:  
To run the server  
`python main.py`   

To run test you should run  
`python -m pytest`  
while in the same directory as main
To create a test add a file under the tests directory using the name of style test_{{name}}.py  
6. optional
You can also setup a incomplete wireguard server by running  
`sudo sh setup/setup_wireguard.py`  
 Note that this wireguard server may not work as intended
 
-------
# To Deploy:

Note only tested on Ubuntu 20.04 server and the wireguard server will not work if you are on the same subnet due to technical limitations of wireguard. All commands below are expected to be run as root user, you can also prepend sudo to each command to run the as root.  
  
1. Clone repositories  
`git clone git@github.com:xlab-classes/cse442-spring2022-team-pyc442.git`  
2. Enter into repositories directory  
`cd cse442-spring2022-team-pyc442`  
3. run setup script and follow prompts  
`sudo sh setup.sh`  
4. enable ufw  
(Must be run as root)  
`ufw allow ssh`  
`ufw allow 'Apache Full'`  
`ufw enable`  
5. Allow ipv4 forwarding  
(must be run as root)  
`sysctl -w net.ipv4.ip_forward=1`  
Warning you will have to run this command after every server restart or you will not have internet access
