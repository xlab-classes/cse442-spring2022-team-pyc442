# cse442-spring2022-team-pyc442  

Pyc442  
Anthony Schiano  
Howie Lin  
Michael Traynor  
Brian Chen  
Michael Lanurias  

to run code use the command Create a virtual environment for python to run  
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

Note only tested on Ubuntu 20.04 server  
  
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
