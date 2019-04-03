from tkinter import Tk, Label
from tkinter.messagebox import showinfo

from ExecutionClass import Execution
from light_control_GUI import ControlLightsGUI


class WaitGui:
    def __init__(self, mode):
        self.dots = 1
        self.time_out = 250
        self.mode = mode
        self.execute = Execution(mode)
        wait_window = Tk()
        wait_window.title("Huejacking")

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
            self.dots = (self.dots % 7) + 1
        else:
            showinfo("Notification", "Congratulations, you're in.")
            self.wait_window.destroy()
            if self.mode >= 1:
                self.control()

    def control(self):
        ControlLightsGUI(self.execute.username, self.execute.ipBridge)
