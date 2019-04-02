import tkinter
import os
import threading
import time
from tkinter import Tk, Label, Button, Frame, LabelFrame, IntVar, colorchooser
from tkinter.messagebox import showinfo
import webbrowser
from tkinter.ttk import Radiobutton

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("MML pro tools")

        self.mode = IntVar()
        self.create_top_frame()
        self.create_bottom_frame()

    def huijack(self):
        self.master.destroy()
        WaitThread(self.mode.get()).run()

    def create_right_frame(self, bottom_frame):
        right_frame = Frame(bottom_frame, pady=20)

        execute_button = Button(right_frame, text="Huejack", command=self.huijack)
        execute_button.pack()

        greet_button = Button(right_frame, text="close", command=self.master.quit)
        greet_button.pack()

        right_frame.grid(row=0, column=1, sticky="nsew")
        return right_frame

    def create_left_frame(self, bottom_frame):
        left_frame = Frame(bottom_frame, pady=20)

        Radiobutton(left_frame, text="Only ARP poisoning", variable=self.mode, value=0).pack(anchor=tkinter.W)
        Radiobutton(left_frame, text="Everything", variable=self.mode, value=1).pack(anchor=tkinter.W)

        left_frame.grid(row=0, column=0, sticky="nsew")
        return left_frame

    def create_top_frame(self):
        top_frame = LabelFrame(self.master)

        label = Label(top_frame, text="Ultimate Philips Hue Hijacking Tool For Pro's!")
        label.pack()

        top_frame.pack()
        return top_frame

    def create_bottom_frame(self):
        bottom_frame = Frame(self.master)
        self.create_left_frame(bottom_frame)
        self.create_right_frame(bottom_frame)

        bottom_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        bottom_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        bottom_frame.grid_rowconfigure(0, weight=1)

        bottom_frame.pack()
        return bottom_frame


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


class WaitThread:
    def __init__(self, mode):
        self.dots = 1
        self.time_out = 250
        self.execute = Execution(mode)
        wait_window = Tk()
        wait_window.title = "Huejacking"

        Label(wait_window, text="Please wait, you are huejacking right now").pack()
        self.wait_animation = Label(wait_window, text=".", font=("Courier", 44))
        self.wait_animation.pack()
        self.wait_window = wait_window

    def run(self):
        self.wait_window.after(self.time_out, self.update)
        self.execute.start()
        self.wait_window.mainloop()

    def update(self):
        if self.execute.isAlive():
            self.wait_window.after(self.time_out, self.update)
            self.wait_animation.config(text="." * self.dots)
            self.dots = (self.dots + 1) % 5
        else:
            if 'mart' in os.getlogin().lower():
                url = 'https://www.youtube.com/watch?v=kkNx12QPpv0'
            else:
                url = "https://www.youtube.com/watch?v=1Bix44C1EzY"
            webbrowser.open_new_tab(url)
            self.wait_window.destroy()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
