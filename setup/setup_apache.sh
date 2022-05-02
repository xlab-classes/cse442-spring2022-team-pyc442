#!/usr/bin/bash

mkdir /var/www/wireguard
cp -r * /var/www/wireguard

chown -r wireguard /var/www/wireguard

read -p "what is the ip/domain name of the server: " IP
read -p "what is the admin email address [webmaster@localhost]: " EMAIL

EMAIL=$(EMAIL:-webmaster@localhost)

systemctl enable apache2
systemctl start apache2

cat > /etc/apache2/sites-available/wireguard.conf << EOF
<VirtualHost *:443>
   	SSLEngine on
   	SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
   	SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin $EMAIL

	WSGIDaemonProcess wireguard user=wireguard group=wireguard threads=5
	WSGIScriptAlias / /var/www/wireguard/wireguard.wsgi

	<Directory /var/www/wireguard>
		WSGIProcessGroup wireguard
		WSGIApplicationGroup %{GLOBAL}
		Require all granted
	</Directory>

	Alias /static /var/www/wireguard/src/app/static
	<Directory /var/www/FlaskApp/FlaskApp/static/>
		Require all granted
	</Directory>


	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>

<VirtualHost *:80>
	Redirect / https://$IP/

</VirtualHost>
EOF

a2enmod wsgi
a2enmod ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt

a2dissite 000-default.conf
a2ensite wireguard.conf
