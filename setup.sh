#! /usr/bin/bash



if [ $EUID -ne 0 ]
then
   echo "this script needs to be run as root"
   exit
fi

sh setup/setup_database.sh
