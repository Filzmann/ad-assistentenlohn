import tkinter as tk
from datetime import datetime

from tkcalendar import Calendar


class AssistentNewEditView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        headline = tk.Label(self, text="Wer bist du denn eigentlich?")
        vorname_label = tk.Label(self, text="Vorname")
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        name_label = tk.Label(self, text="Nachname")
        self.name_input = tk.Entry(self, bd=5, width=40)
        email_label = tk.Label(self, text="Email")
        self.email_input = tk.Entry(self, bd=5, width=40)
        strasse_label = tk.Label(self, text="Straße/Hausnummer")
        self.strasse_input = tk.Entry(self, bd=5, width=29)
        self.hausnummer_input = tk.Entry(self, bd=5, width=9)
        plz_label = tk.Label(self, text="Postleitzahl")
        self.plz_input = tk.Entry(self, bd=5, width=40)
        stadt_label = tk.Label(self, text="Stadt")
        self.stadt_input = tk.Entry(self, bd=5, width=40)
        einstellungsdatum_label = tk.Label(self, text="Seit wann bei ad? (tt.mm.JJJJ)")
        self.einstellungsdatum_input = Calendar(self)
        self.save_button = tk.Button(self, text="Daten speichern")
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)


        # ins Fenster packen
        headline.grid(row=0, column=0, columnspan=3)
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        name_label.grid(row=2, column=0)
        self.name_input.grid(row=2, column=1, columnspan=2)
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)
        strasse_label.grid(row=4, column=0)
        self.strasse_input.grid(row=4, column=1)
        self.hausnummer_input.grid(row=4, column=2)
        plz_label.grid(row=5, column=0)
        self.plz_input.grid(row=5, column=1, columnspan=2)
        stadt_label.grid(row=6, column=0)
        self.stadt_input.grid(row=6, column=1, columnspan=2)
        einstellungsdatum_label.grid(row=7, column=0, sticky="nw")
        self.einstellungsdatum_input.grid(row=7, column=1)

        self.exit_button.grid(row=8, column=0)
        self.save_button.grid(row=8, column=1)

    def set_data(self, **kwargs):
        self.vorname_input.insert(0, kwargs['vorname'])
        self.name_input.insert(0, kwargs['name'])
        self.email_input.insert(0, kwargs['email'])
        self.strasse_input.insert(0, kwargs['strasse'])
        self.hausnummer_input.insert(0, kwargs['hausnummer'])
        self.plz_input.insert(0, kwargs['plz'])
        self.stadt_input.insert(0, kwargs['stadt'])
        self.einstellungsdatum_input.selection_set(kwargs['einstellungsdatum'])

    def get_data(self):
        einstellungsdatum_date_obj = datetime.strptime(self.einstellungsdatum_input.get_date(), '%m/%d/%y')

        return {
            'name': self.name_input.get(),
            'vorname': self.vorname_input.get(),
            'email': self.email_input.get(),
            'einstellungsdatum': einstellungsdatum_date_obj,
            'strasse': self.strasse_input.get(),
            'hausnummer': self.hausnummer_input.get(),
            'plz': self.plz_input.get(),
            'stadt': self.stadt_input.get()
        }
