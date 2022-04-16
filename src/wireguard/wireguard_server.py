import subprocess
import ipaddress
from src.database import wireguard_db

class Wireguard_Server():

    _running: bool = False
    _public_key: str = ""

    def __init__(self):
        # set the running bool to false
        self._running = False

        #get public key and save
        pubkey = subprocess.run(['sudo', 'cat', '/etc/wireguard/public.key'], capture_output=True)

        self._public_key = pubkey.stdout.decode().strip()


    def start(self) -> None:
        if not self._running:
            subprocess.run(['sudo', 'wg-quick', 'up', 'wg0'])
            self._running = True


    def stop(self) -> None:
        if self._running:
            subprocess.run(['sudo', 'wg-quick', 'down', 'wg0'])
            self._running = False


    def is_running(self) -> bool:
        return self._running

    def get_pubkey(self) -> str:
        return self._public_key

    def add_user_new(self, uid: str) -> bool:

        # error checking, uid must exist in and not have a public private key pair already
        if wireguard_db.getUserById(uid) == None or wireguard_db.get_user_server(uid) != None:
            return False

        wasnotrunning = False

        if not self.is_running:
            self.start()
            wasnotrunning = True
        # generate keys for user
        # create private key
        privkey = subprocess.run(['wg', 'genkey'], capture_output=True)
        # make private key pipeable so that wg pubkey | echo <private key> works as expected
        pipe = subprocess.Popen(['echo', privkey.stdout], stdout=subprocess.PIPE)
        # create the public key
        pubkey = subprocess.run(['wg', 'pubkey'], capture_output=True, stdin=pipe.stdout)

        # get the ip address for the new user
        # get the current last allocated ip
        maxip = wireguard_db.get_max_ip()
        ip = 0

        # if the maxip is none then there is no allocated ip so allocate it to the first one available 10.8.0.2 otherwise add 1 to the max ip to get a new unique ip
        if maxip == None:
            ip = int(ipaddress.ip_address('10.8.0.2'))
        else:
            ip = maxip + 1

        # add users key pair into database
        wireguard_db.add_user_server(uid, privkey.stdout.decode(), pubkey.stdout.decode(), ip)

        subprocess.run(['sudo', 'wg', 'set', 'wg0', 'peer', pubkey.stdout.decode().strip(), 'allowed-ips', str(ipaddress.ip_address('10.8.0.0')) + '/24'])

        if wasnotrunning:
            self.stop()

        return True

