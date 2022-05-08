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
echo 51820 > /etc/wireguard/port

# the base configuration for the server
# write the config out to file
cat > /etc/wireguard/wg0.conf << EOL
[Interface]
Address = 10.8.0.1/24
SaveConfig = true
PostUp = iptables -A FORWARD -i $DEV -o wg0 -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o $DEV -j MASQUERADE; ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o $DEV -j MASQUERADE; ufw route allow in on wg0 out on $DEV; ufw route allow in on $DEV out on wg0
PostDown = iptables -D FORWARD -i $DEV -o wg0 -j ACCEPT; iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o $DEV -j MASQUERADE; ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o $DEV -j MASQUERADE; ufw route delete allow in on wg0 out on $DEV; ufw route delete allow in on $DEV out on wg0;
ListenPort = 51820
PrivateKey = $PRIVKEY
EOL

chown -R wireguard /etc/wireguard
