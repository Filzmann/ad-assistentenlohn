import tkinter as tk
from hauptfenster import Hauptfenster
from person import AS


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.assistent = AS()
        self.geometry('{}x{}'.format(1200, 600))
        self.title("Dein Assistentenlohn")
        self.config(menu="")
        self.fenster = Hauptfenster(self, self.assistent, borderwidth=3, relief="ridge")
        self.fenster.grid(row=0, column=0, sticky=tk.NSEW)
        self.fenster.config(height=1000)


if __name__ == "__main__":
    root = App()
    root.mainloop()
