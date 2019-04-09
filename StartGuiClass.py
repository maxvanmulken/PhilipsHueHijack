import os
import tkinter
from tkinter import Label, Button, Frame, LabelFrame, IntVar, Radiobutton

from WaitGuiClass import WaitGui
from light_control_GUI import ControlLightsGUI


class StartGui:
    def __init__(self, master):
        self.master = master
        master.title("MML pro tools")

        self.mode = IntVar()
        self.create_top_frame()
        self.create_bottom_frame()

    def huejack(self):
        self.master.destroy()

        ControlLightsGUI('KIyuOC6iDM2i52oYIdeFcDOE4PCcr8jQMB4Jxm1p', '192.168.178.178')
        #WaitGui(self.mode.get()).run()

    def create_right_frame(self, bottom_frame):
        right_frame = Frame(bottom_frame, pady=20)

        execute_button = Button(right_frame, text="Huejack", command=self.huejack)
        execute_button.pack()

        greet_button = Button(right_frame, text="Close", command=self.master.quit)
        greet_button.pack()

        right_frame.grid(row=0, column=1, sticky="nsew")
        return right_frame

    def create_left_frame(self, bottom_frame):
        left_frame = Frame(bottom_frame, pady=20)

        Radiobutton(left_frame, text="Deny service", variable=self.mode, value=0).pack(anchor=tkinter.W)
        Radiobutton(left_frame, text="Hijack control", variable=self.mode, value=1).pack(anchor=tkinter.W)

        left_frame.grid(row=0, column=0, sticky="nsew")
        return left_frame

    def create_top_frame(self):
        top_frame = LabelFrame(self.master)

        label_string = "Huejacking tool made by Port 25565\nLuuk Schuurmans, Mart Hagedoorn, Max van Mulken"
        label = Label(top_frame, text=label_string)
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
