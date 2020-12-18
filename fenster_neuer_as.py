import tkinter as tk
from tkcalendar import Calendar
import datetime
from person import AS, Adresse


class FensterNeuerAS(tk.Toplevel):
    def __init__(self, parent, assistent,  edit=0):
        super().__init__(parent)
        self.parent = parent
        self.assistent = assistent
        self.edit = edit
        headline = tk.Label(self, text="Wer bist du denn eigentlich?")
        vorname_label = tk.Label(self, text="Vorname")
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        nachname_label = tk.Label(self, text="Nachname")
        self.nachname_input = tk.Entry(self, bd=5, width=40)
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
        self.save_button = tk.Button(self, text="Daten speichern", command=self.action_save_neuer_as)
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)

        if edit:
            self.vorname_input.insert(0, self.assistent.vorname)
            self.nachname_input.insert(0, self.assistent.name)
            self.email_input.insert(0, self.assistent.email)
            self.strasse_input.insert(0, self.assistent.home.strasse)
            self.hausnummer_input.insert(0, self.assistent.home.hnr)
            self.plz_input.insert(0, self.assistent.home.plz)
            self.stadt_input.insert(0, self.assistent.home.stadt)

        # ins Fenster packen
        headline.grid(row=0, column=0, columnspan=3)
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        nachname_label.grid(row=2, column=0)
        self.nachname_input.grid(row=2, column=1, columnspan=2)
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)
        strasse_label.grid(row=4, column=0)
        self.strasse_input.grid(row=4, column=1)
        self.hausnummer_input.grid(row=4, column=2)
        plz_label.grid(row=5, column=0)
        self.plz_input.grid(row=5, column=1, columnspan=2)
        stadt_label.grid(row=6, column=0)
        self.stadt_input.grid(row=6, column=1, columnspan=2)

        # TODO Text nach oben
        einstellungsdatum_label.grid(row=7, column=0)
        self.einstellungsdatum_input.grid(row=7, column=1)
        self.exit_button.grid(row=8, column=0)
        self.save_button.grid(row=8, column=1)

    def action_save_neuer_as(self):
        einstellungsdatum_date_obj = datetime.datetime.strptime(self.einstellungsdatum_input.get_date(),
                                                                '%m/%d/%y')
        assistent = AS(self.nachname_input.get(), self.vorname_input.get(),
                       self.email_input.get(), einstellungsdatum_date_obj)
        assistent.home = Adresse(kuerzel='home',
                                 strasse=self.strasse_input.get(),
                                 hnr=self.hausnummer_input.get(),
                                 plz=self.plz_input.get(),
                                 stadt=self.stadt_input.get())
        assistent.__class__.assistent_is_loaded = 1

        neu = 0 if self.edit == 1 else 1
        assistent.save_to_file(neu=neu)
        self.parent.fenster.redraw(assistent)
        self.destroy()
