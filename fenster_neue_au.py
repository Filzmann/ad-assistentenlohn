import tkinter as tk
from tkcalendar import Calendar
import datetime
from arbeitszeit import Arbeitsunfaehigkeit


class NeueAU(tk.Toplevel):
    def __init__(self, parent, assistent):
        super().__init__(parent)
        self.assistent = assistent
        self.parent = parent
        self.headline = tk.Label(self, text="AU/krank eintragen")
        self.startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.urlaubsstatus = tk.StringVar()
        self.urlaubsstatus.set('notiert')

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neue_arbeitsunfaehigkeit)
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)
        self.saveandnew_button = tk.Button(self,
                                           text="Daten speichern und neu",
                                           command=lambda: self.action_save_neue_arbeitsunfaehigkeit(undneu=1))

        # ins Fenster packen
        self.headline.grid(row=0, column=0, columnspan=4)
        self.startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        self.enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def action_save_neue_arbeitsunfaehigkeit(self, undneu=0):

        startdatum = self.startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = self.enddatum_input.get_date().split('/')
        # au geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)

        # au erstellen und zum Assistenten stopfen
        au = Arbeitsunfaehigkeit(beginn=beginn, ende=ende, assistent=self.assistent)
        self.assistent.au_dazu(au)
        self.assistent.save_to_file()
        self.destroy()
        if undneu == 1:
            NeueAU(self.parent, self.assistent)
