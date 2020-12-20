import tkinter as tk
from tkcalendar import Calendar
import datetime
from arbeitszeit import Urlaub


class NeuerUrlaub(tk.Toplevel):
    def __init__(self, parent, assistent):
        super().__init__(parent)
        self.parent = parent
        self.assistent = assistent
        self.headline = tk.Label(self, text="Urlaub eintragen")
        self.startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.urlaubsstatus = tk.StringVar()
        self.urlaubsstatus.set('notiert')
        self.status_label = tk.Label(self, text="Status")
        self.status_input_radio1 = \
            tk.Radiobutton(self, text="notiert", padx=20,
                           variable=self.urlaubsstatus, value='notiert')
        self.status_input_radio2 = \
            tk.Radiobutton(self, text="beantragt", padx=20,
                           variable=self.urlaubsstatus, value='beantragt')
        self.status_input_radio3 = \
            tk.Radiobutton(self, text="genehmigt", padx=20,
                           variable=self.urlaubsstatus, value='genehmigt')

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neuer_urlaub)
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu",
                                           command=lambda: self.action_save_neuer_urlaub(undneu=1))

        # ins Fenster packen
        self.headline.grid(row=0, column=0, columnspan=4)
        self.startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        self.enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        self.status_label.grid(row=3, column=0)

        self.status_input_radio1.grid(row=3, column=1)
        self.status_input_radio2.grid(row=3, column=2)
        self.status_input_radio3.grid(row=3, column=3)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def action_save_neuer_urlaub(self, undneu=0):

        startdatum = self.startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = self.enddatum_input.get_date().split('/')
        # urlaub geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)
        status = self.urlaubsstatus.get()

        # Schicht erstellen und zum Assistenten stopfen
        urlaub = Urlaub(beginn=beginn, ende=ende, status=status, assistent=self.assistent)
        self.assistent.urlaub_dazu(urlaub)
        self.assistent.save_to_file()
        self.destroy()
        self.parent.fenster.redraw(self.assistent)
        if undneu == 1:
            NeuerUrlaub(self.parent, self.assistent)
