#!/usr/bin/bash

apt install mysql-server -y

systemctl enable mysql
systemctl start mysql

#mysql_secure_installation -u root --use-default
mysql -e "DROP USER IF EXISTS ''@'localhost'; DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -e "DROP DATABASE IF EXISTS test; DELETE FROM mysql.db WHERE Db='test' or Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES"

echo "{\"username\": \"wireguard\", \"password\": \"$1\"}" > database.cfg


mysql -u root -e "CREATE USER IF NOT EXISTS 'wireguard'@'localhost' IDENTIFIED BY '$1';"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS wireguard DEFAULT CHARACTER SET 'utf8';"
mysql -u root -e "GRANT SELECT, INSERT, UPDATE, DELETE ON wireguard.* TO 'wireguard'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"
mysql -u root -e "USE wireguard; CREATE TABLE IF NOT EXISTS wireguard (
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
) ENGINE=InnoDB;"

systemctl restart mysql
