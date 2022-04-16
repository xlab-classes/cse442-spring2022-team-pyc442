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
CONFIG_FILE="[Interface]\nAddress = 10.8.0.1/24\nSaveConfig = true\nPostUp = iptables -t nat -I POSTROUTING -o $DEV -j MASQUERADE\nPostUp = iptables -I INPUT 1 -i wg0 -j ACCEPT\nPostUp = iptables -I FORWARD 1 -i $DEV -o wg0 -j ACCEPT\nPostUp = iptables -I FORWARD 1 -i wg0 -o $DEV -j ACCEPT\nPreDown = iptables -t nat -D POSTROUTING -o $DEV -j MASQUERADE\nPreDown = iptables -D INPUT -i wg0 -j ACCEPT\nPreDown = iptables -D FORWARD -i $DEV -o wg0 -j ACCEPT\nPreDown = iptables -D FORWARD -i wg0 -o $DEV -j ACCEPT\nListenPort = 51820\nPrivateKey = $PRIVKEY\n
"

# write the config out to file
echo -e $CONFIG_FILE > /etc/wireguard/wg0.conf

#allow IPv4 forwarding
sysctl -w net.ipv4.ip_forward=1
