import tkinter as tk
from View.begruessungs_view import BegruessungsView


class MainView(tk.Tk):
    inhalt = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(1200, 600))
        self.title("Dein Assistentenlohn")
        self.config(menu="")

    def draw_begruessung(self):
        for child in self.winfo_children():
            child.destroy()

        self.inhalt = BegruessungsView(self)
        self.inhalt.grid(row=0, column=0)





