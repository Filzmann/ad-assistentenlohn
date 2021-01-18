import tkinter as tk


class SummenView(tk.Frame):
    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        tk.Label(self, text='Summen').grid(row=0, column=0)