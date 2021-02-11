import tkinter as tk
from datetime import datetime


class NavigationView(tk.Frame):
    def __init__(self, parent_view, init_date=None):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)

        self.akt_date = init_date if init_date else datetime.now()
        self.parent = parent_view
        # self.offset = offset
        # self.assistent = assistent
        # offset = 0
        self.vormonat = tk.Button(self, text='einen Monat Zurück')
        self.arbeitsdate = self.akt_date
        # self.parent.seitenleiste.arbeitsdatum = self.arbeitsdate
        self.aktueller_monat = tk.Label(self, text=self.arbeitsdate.strftime("%B %Y"))
        self.naechster_monat = tk.Button(self, text='Nächster Monat')
        self.draw()

    def draw(self):
        # in den frame packen
        self.vormonat.grid(row=0, column=0, sticky="w")
        self.aktueller_monat.grid(row=0, column=1)
        self.naechster_monat.grid(row=0, column=2, sticky="e")
