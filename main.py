import tkinter as tk
from hauptfenster import Hauptfenster
from person import AS


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.assistent = AS()
        self.geometry('1200x800')
        self.title("Dein Assistentenlohn")
        self.config(menu="")
        self.fenster = Hauptfenster(self, self.assistent)
        self.fenster.pack()


if __name__ == "__main__":
    root = App()
    root.mainloop()
