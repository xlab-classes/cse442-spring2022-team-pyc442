#!/usr/bin/bash

useradd -m wireguard

echo 'wireguard ALL=NOPASSWD: /usr/bin/wg, /usr/bin/wg-quick, /usr/bin/cat' >> /etc/sudoers
