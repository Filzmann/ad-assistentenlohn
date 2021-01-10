import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar


class AUView(tk.Toplevel):
    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.parent = parent_view
        self.title('AU/krank Eintragen')
        startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')

        self.save_button = tk.Button(self, text="Daten speichern")
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu")

        # ins Fenster packen
        startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def set_data(self, **kwargs):
        self.startdatum_input.selection_set(kwargs['beginn'])
        self.enddatum_input.selection_set(kwargs['ende'])

    def get_data(self):
        startdatum_date_obj = datetime.strptime(self.startdatum_input.get_date(), '%m/%d/%Y')
        enddatum_date_obj = datetime.strptime(self.enddatum_input.get_date(), '%m/%d/%Y')

        return {
            'beginn': startdatum_date_obj,
            'ende': enddatum_date_obj
        }
