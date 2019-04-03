from tkinter import Tk, Label, Button, Frame, Checkbutton, IntVar, Scale, HORIZONTAL
from tkinter.messagebox import showinfo
from tkinter.ttk import Style

from scripts.LightClass import Light


class ControlLightsGUI:

    def __init__(self):
        self.control_lights = Tk()
        self.control_lights.configure(background="black")
        self.green_color = "#20C20E"
        self.control_lights.title("MML pro tools")

        self.lights = [
            Light(0, "Light 1", True, "#00ffff"),
            Light(1, "Light 2", True, "#00ffff"),
            Light(2, "Light 3", True, "#00ffff"),
            Light(3, "Light 4", True, "#00ffff"),
        ]

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
                text="Toggle light"
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
        light.set('selected', selected)

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
