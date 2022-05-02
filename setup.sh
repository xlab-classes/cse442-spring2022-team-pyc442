#! /usr/bin/bash



if [ $EUID -ne 0 ]
then
   echo "this script needs to be run as root or using sudo"
   exit
fi

# download and install all the packages necessary
apt update
apt install -y mysql-server virtualenv python3 python-is-python3 apache2 openssl wireguard libapache2-mod-wsgi-py3

USER_PASSWD=$(gpg --gen-random --armor 1 14)

sh setup/setup_database.sh $USER_PASSWD
sh setup/setup_user.sh
sh setup/setup_python.sh
sh setup/setup_wireguard.sh
. venv/bin/activate
python setup/setup_admin_user.py $USER_PASSWD

sh setup/setup_apache.sh
