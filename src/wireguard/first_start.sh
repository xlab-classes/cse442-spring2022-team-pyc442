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
# sorry for how hard this is to read but bash wasnt letting me do muliline strings
CONFIG_FILE="[Interface]\nAddress = 10.8.0.1/32\nSaveConfig = true\nPostUp = ufw enable\nPostUp = sysctl -w net.ipv4.ip_forward=1\nPostUp = iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE\nPostUp = ufw route allow in on wg0 out on $DEV\nPreDown = ufw route delete allow in on wg0 out on $DEV\nPreDown = iptables -t nat -D POSTROUTING -o $DEV -j MASQUERADE\nPreDown = sysctl -w net.ipv4.ip_forward=0\nListenPort = 51820\nPrivateKey = $PRIVKEY\n"
# write the config out to file
echo -e $CONFIG_FILE > /etc/wireguard/wg0.conf

