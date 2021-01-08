import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar


class UrlaubView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        headline = tk.Label(self, text="Urlaub eintragen")
        startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.urlaubsstatus = tk.StringVar()
        self.urlaubsstatus.set('notiert')
        status_label = tk.Label(self, text="Status")
        status_input_radio1 = \
            tk.Radiobutton(self, text="notiert", padx=20,
                           variable=self.urlaubsstatus, value='notiert')
        status_input_radio2 = \
            tk.Radiobutton(self, text="beantragt", padx=20,
                           variable=self.urlaubsstatus, value='beantragt')
        status_input_radio3 = \
            tk.Radiobutton(self, text="genehmigt", padx=20,
                           variable=self.urlaubsstatus, value='genehmigt')

        self.save_button = tk.Button(self, text="Daten speichern")
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu")

        # ins Fenster packen
        headline.grid(row=0, column=0, columnspan=4)
        startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        status_label.grid(row=3, column=0)

        status_input_radio1.grid(row=3, column=1)
        status_input_radio2.grid(row=3, column=2)
        status_input_radio3.grid(row=3, column=3)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def set_data(self, **kwargs):
        self.startdatum_input.selection_set(kwargs['beginn'])
        self.enddatum_input.selection_set(kwargs['ende'])
        self.urlaubsstatus.set(kwargs['status'])

    def get_data(self):
        test = self.startdatum_input.get_date()
        startdatum_date_obj = datetime.strptime(self.startdatum_input.get_date(), '%m/%d/%Y')
        enddatum_date_obj = datetime.strptime(self.enddatum_input.get_date(), '%m/%d/%Y')

        return {
            'beginn': startdatum_date_obj,
            'ende': enddatum_date_obj,
            'status': self.urlaubsstatus.get(),
        }
