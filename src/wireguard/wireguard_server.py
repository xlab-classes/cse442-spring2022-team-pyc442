import subprocess
import os

class Wireguard_Server():
    _running = False

    def start(self):
        if not self._running:
            subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1'])
            subprocess.run(['sudo', 'wg-quick', 'up', 'wg0'])
            self._running = True

    def stop(self):
        if self._running:
            subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=0'])
            subprocess.run(['sudo', 'wg-quick', 'down', 'wg0'])
            self._running = False

    def is_running(self):
        return self._running

if __name__ == '__main__':
    wg = Wireguard_Server()
    wg.start()
    wg.stop()
