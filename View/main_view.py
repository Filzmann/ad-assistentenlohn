import tkinter as tk
from View.begruessungs_view import BegruessungsView


class MainView(tk.Tk):
    inhalt: tk.Frame = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(1200, 600))
        self.title("Dein Assistentenlohn")
        self.config(menu="")
        if self.inhalt:
            self.inhalt.grid(row=0, column=0, sticky=tk.NW)
