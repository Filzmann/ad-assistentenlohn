import tkinter as tk


class HauptseiteView(tk.Frame):
    navigation: tk.Frame = None
    tabelle: tk.Frame = None
    summen: tk.Frame = None
    infotext: tk.Frame = None

    def __init__(self, parent_view, as_name=''):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        hallo = Title(self, as_name)

        hallo.grid(row=0, column=1)
        self.draw()

    def draw(self):
        if self.navigation:
            self.navigation.grid(row=0, column=0)
        if self.tabelle:
            self.tabelle.grid(row=1, column=0, rowspan=2, sticky=tk.NW)
        if self.summen:
            self.summen.grid(row=1, column=1)
        if self.infotext:
            self.infotext.grid(row=2, column=1)


class Title(tk.Frame):
    def __init__(self, parent, as_name):
        super().__init__(parent)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        hallo = tk.Label(self, text="Hallo " + as_name)
        hallo.grid(row=0, column=0)


