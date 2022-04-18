# cse442-spring2022-team-pyc442  

Pyc442  
Anthony Schiano  
Howie Lin  
Michael Traynor  
Brian Chen  
Michael Lanurias  

to run code use the command
Create a virtual environment for python to run  
`python -m venv env`  
Then install the proper libraries  
`pip install -r requirements.txt`  
or `python -m pip install -r requirements.txt`  
then  
`python main.py`  

To run test you should run  
`python -m pytest`  
while in the same directory as main  
To create a test add a file under the tests directory using the name of style test_{{name}}.py  

To Deploy:

Note only test on ubuntu 20.04 server  
  
1. Clone repositories  
`git clone git@github.com:xlab-classes/cse442-spring2022-team-pyc442.git`  
2. install dependencies  
`sudo apt install python3-virtualenv libapache2-mod-wsgi python3 python-is-python3 mysql-server`  
3. setup database  
`sudo mysql_secure_installation`  
follow the prompts to setup your database as you would like
4. give the server the password for the root database user
`cd cse442-spring2022-team-pyc442`  
Please do not leave this directory for the duration of the setup
`nano src/database/wireguard.py`  
edit the line with DB_PASSWORD = "password" to DB_PASSWORD = "<your password>" where <your password> is the password you created  
5. create a virtual python environment  
`virtualenv venv`  
6. source the environment and install python dependencies  
`source venv/bin/activate`  
`pip install -r requirements.txt`
7. run the script that creates wireguard server config  
`sudo ./src/wireguard/first_start.sh`  
Dont forget to enter your password in if it requests one  
8. setup apache  
please follow the setup guide here https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/  
please note that you will be expected to move your files into /var/www/wireguard/ if you want to use the provided wireguard.wsgi file otherwise you will have to create your own  
please make sure config file in /etc/apache/sites-available is named wireguard.conf or you will have to edit commands  
to create correct file use 
`sudo nano /etc/apache/sites-available/wireguard.conf`  
this command will allow you to edit the file before creating it  

to move file you can  
`sudo mkdir /var/www/wireguard`  
`sudo cp -r * /var/www/wireguard/`  


9. apache ssl (optional)  
please follow this guide https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-20-04 if you have a domain name you would like to used  
If you don not have a domain name use https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04  
the wireguard.wsgi file will work for this in cse442-spring2022-team-pyc442  
10. activate mysql  

`sudo systemctl enable mysql`  
`sudo systemctl start mysql`  

11. start apache  

`sudo a2enmod wsgi`  
`sudo a2dissite 000-default.conf`  
`sudo a2ensite wireguard.conf`  
`sudo systemctl enable apache2`  
`sudo systemctl start apache2`

optional:  
`sudo a2enmod ssl`  
