#!/bin/bash

# set the umask so that files are created with the correct permissions
umask 077

# create the directory and files for wirguard config
mkdir /etc/wireguard
touch /etc/wireguard/private.key
touch /etc/wireguard/public.key

# create the public and private key for the wireguard server
wg genkey > /etc/wireguard/private.key
cat /etc/wireguard/private.key | wg pubkey > /etc/wireguard/public.key

# store the wireguard private key in a variable for later use
PRIVKEY=$(cat /etc/wireguard/private.key)

# get default device for routing internet traffic
DEV=$(ip route list default | awk '{print $5}')

# the base configuration for the server
# write the config out to file
cat > /etc/wireguard/wg0.conf << EOL
[Interface]\n
Address = 10.8.0.1/24\n
SaveConfig = true\n
PostUp = ufw route allow in on wg0 out on $DEV\n
PostUp = ufw route allow in on $DEV out on wg0\n
PostUp =  ufw allow proto udp from any to any port 51820\n
PostUp = sysctl -w net.ipv4.ip_forward=1\n
PostUp = iptables -t nat -I POSTROUTING -o $DEV -j MASQUERADE\n
PreDown = iptables -t nat -D POSTROUTING -o $DEV -j MASQUERADE\n
PostDown = ufw route delete allow in on wg0 out on eth0\n
PostDown = ufw route delete allow in on eth0 out on wg0\n
PostDown = ufw delete allow proto udp from any to any port 51820\n
PreDown = sysctl -w net.ipv4.ip_forward=0\n
ListenPort = 51820\n
PrivateKey = $PRIVKEY\n
EOL

