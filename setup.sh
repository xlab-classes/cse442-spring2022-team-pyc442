#! /usr/bin/bash



if [ $EUID -ne 0 ]
then
   echo "this script needs to be run as root or using sudo"
   exit
fi

# download and install all the packages necessary
apt update
apt install -y mysql-server virtualenv python3 python-is-python3 apache2 openssl wireguard

sh setup/setup_database.sh
sh setup/setup_user.sh
python setup_admin_user.py
