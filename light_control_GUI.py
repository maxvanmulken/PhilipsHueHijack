import json
from tkinter import Tk, Label, Button, Frame, Checkbutton, IntVar, Scale, HORIZONTAL
import numpy as np
from tkinter.messagebox import showinfo
from tkinter.ttk import Style

import requests

from LightClass import Light


class ControlLightsGUI:

    def __init__(self, username, ipBridge):
        self.control_lights = Tk()
        self.control_lights.configure(background="black")
        self.green_color = "#20C20E"
        self.control_lights.title("MML pro tools")

        self.username = username
        self.ipBridge = ipBridge
        self.link = 'http://' + self.ipBridge + "/api/" + self.username

        self.lights = []

        response_lights = requests.get(self.link + "/lights/new")
        response_lights_dict = json.loads(response_lights.content)

        for key, value in response_lights_dict.items():
            if key != 'lastscan':
                response_light = requests.get(self.link + "/lights/" + str(key))
                response_light_dict = json.loads(response_light.content)

                xy = list(response_light_dict['state']['xy'])
                bri = int(response_light_dict['state']['bri'])
                on = bool(response_light_dict['state']['on'])

                rgb = convert_xy_to_rgb(xy, bri)
                print(rgb)
                self.lights.append(Light(key, value['name'], on, rgb))

        self.create_left_frame(self.control_lights)
        self.create_middle_frame(self.control_lights)
        self.create_right_frame(self.control_lights)

        self.control_lights.grid_columnconfigure(0, weight=1, uniform="group1")
        self.control_lights.grid_columnconfigure(1, weight=1, uniform="group1")
        self.control_lights.grid_rowconfigure(0, weight=1)

    def create_left_frame(self, master):
        left_window = Frame(master, background="black")

        self.create_left_top_frame(left_window)
        self.create_left_bottom_frame(left_window)

        left_window.grid(row=0, column=0, sticky="nsew")

    def create_left_top_frame(self, master):
        left_top_window = Frame(master)

        buttons = [
            Button(
                left_top_window,
                text="Pick color"
            ),
            Button(
                left_top_window,
                text="Toggle light",
                command=self.toggle_lights
            )
        ]
        self.style_buttons(buttons)

        left_top_window.pack()

    def create_left_bottom_frame(self, master):
        left_bottom_frame = Frame(master, bg="black")

        for light in self.lights:
            self.create_light_widget(left_bottom_frame, light)

        left_bottom_frame.pack()

    def create_light_widget(self, master, light):
        v = IntVar()

        light_checkbox = Checkbutton(
            master,
            text=light.get('name'),
            variable=v,
            command=lambda: self.select_light(light, v),
            bg="black",
            fg=self.green_color,
            activebackground="black",
            activeforeground=self.green_color,
        )

        light_state = Frame(
            master,
            width=32,
            height=32,
            bg=light.get("color"),
            bd=2,
            highlightbackground="white",
            highlightcolor="white",
            highlightthickness=2,
        )

        light_checkbox.grid(row=light.get('id'), column=0, pady=2)
        light_state.grid(row=light.get('id'), column=1, pady=2)

    @staticmethod
    def select_light(light, selected):
        print(selected.get())
        light.set('selected', selected.get())

    def toggle_lights(self):
        for light in self.lights:
            print(light.get('id'))
            light.toggle(self.ipBridge, self.username)

    def create_middle_frame(self, master):
        middle_frame = Frame(master, bg="black")

        Scale(
            middle_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            bg="black",
            fg=self.green_color,
            activebackground=self.green_color,
            highlightcolor=self.green_color,
            sliderlength=20
        ).pack()

        Label(
            middle_frame,
            text="Brightness",
            fg=self.green_color,
            bg="black"
        ).pack()

        middle_frame.grid(row=0, column=1, sticky="nsew")

    def create_right_frame(self, master):
        right_window = Frame(master, background="black")
        buttons = [
            Button(
                right_window,
                text="Rainbow Gay Mode",
            ),
            Button(
                right_window,
                text="Disco mode",
            ),
            Button(
                right_window,
                text="Send alert",
            ),
        ]
        self.style_buttons(buttons)
        right_window.grid(row=0, column=2, sticky="nsew")

    def style_buttons(self, buttons):
        for button in buttons:
            button.config(
                fg="white",
                background=self.green_color,
                activebackground="green4",
                activeforeground="white",
                borderwidth=5,
                width=20,
                height=2,
            )
            button.pack()


def convert_xy_to_rgb(xy, brightness):
    x = xy[0]
    y = xy[1]
    z = 1.0 - x - y
    Y = float(brightness) / 255
    X = (Y / y) * x
    Z = (Y / y) * z
    r =  X * 1.656492 - Y * 0.354851 - Z * 0.255038
    g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
    b =  X * 0.051713 - Y * 0.121364 + Z * 1.011530

    r = 12.92 * r if r <= 0.0031308 else (1.0 + 0.055) * np.power(r, (1.0 / 2.4)) - 0.055
    g = 12.92 * g if g <= 0.0031308 else (1.0 + 0.055) * np.power(g, (1.0 / 2.4)) - 0.055
    b = 12.92 * b if b <= 0.0031308 else (1.0 + 0.055) * np.power(b, (1.0 / 2.4)) - 0.055

    maxValue = np.max([r, g, b])

    r /= maxValue
    g /= maxValue
    b /= maxValue

    r = r * 255
    if r < 0:
        r = 255

    g = g * 255
    if g < 0:
        g = 255

    b = b * 255
    if b < 0:
        b = 255

    r = hex(int(np.round(r)))[2:]
    g = hex(int(np.round(g)))[2:]
    b = hex(int(np.round(b)))[2:]

    if len(r) < 2:
        r = "0" + r
    if len(g) < 2:
        g = "0" + g
    if len(b) < 2:
        b = "0" + b
    rgb = "#" + r + g + b

    return rgb