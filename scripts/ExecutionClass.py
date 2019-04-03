import threading
import time

from scripts.Functions import clear


class Execution(threading.Thread):

    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        return

    def setup(self):
        # todo
        print("SETUP")
        print("===============")

        return

    def run(self):
        clear()
        print("===============")
        print("Starting attack")
        print("===============")
        self.setup()

        time.sleep(3)

        if self.mode >= 0:
            self.do_arp_posioning()

        if self.mode >= 1:
            self.do_more()

        self.finalize()
        print("===============")
        print("Attack ended")
        print("===============")

    def do_arp_posioning(self):
        print("ARP the bitch")
        return

    def do_more(self):
        print("And more!")
        return

    def finalize(self):

        return
