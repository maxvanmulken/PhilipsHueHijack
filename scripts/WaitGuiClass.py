from tkinter import Tk, Label

from scripts.ExecutionClass import Execution


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
            self.wait_window.destroy()
