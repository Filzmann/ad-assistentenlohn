import tkinter as tk
from datetime import datetime

from Helpers.combobox_dict import Combobox


class NavigationView(tk.Frame):
    def __init__(self, parent_view, init_date=None, **kwargs):
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

        self.selected_month = tk.IntVar()

        if 'monatsarray' in kwargs:
            self.monats_dropdown = Combobox(self, values=kwargs['monatsarray'], width=5, state="readonly")
        if 'jahrarray' in kwargs:
            self.jahr_dropdown = Combobox(self, values=kwargs['jahrarray'], width=5, state="readonly")
            self.changebutton = tk.Button(self, text='Go!')
        self.draw()

    def draw(self):
        # in den frame packen
        self.vormonat.grid(row=0, column=0, sticky="w")
        self.aktueller_monat.grid(row=0, column=1)
        self.naechster_monat.grid(row=0, column=2, sticky="e")
        spacer = tk.Label(master=self, text='', width=20).grid(row=0, column=3)
        if hasattr(self, 'monats_dropdown'):
            self.monats_dropdown.grid(row=0, column=4)
        
        if hasattr(self, 'jahr_dropdown'):
            self.jahr_dropdown.grid(row=0, column=5)
            self.changebutton.grid(row=0, column=6)

