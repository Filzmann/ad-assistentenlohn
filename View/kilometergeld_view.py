import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar

from Helpers.combobox_dict import Combobox


class KilometergeldView(tk.Toplevel):
    def __init__(self, parent_view, **kwargs):
        super().__init__(parent_view)
        self.parent = parent_view

        if 'jahrarray' in kwargs:
            self.jahr_dropdown = Combobox(self, values=kwargs['jahrarray'], width=5, state="readonly")
            self.changebutton = tk.Button(self, text='Go!')

        self.u8 = tk.Label(master=self, text=str(kwargs['data']['<=8']))
        self.ue8 = tk.Label(master=self, text=str(kwargs['data']['>8']))
        self.ue24 = tk.Label(master=self, text=str(kwargs['data']['>24']))

        self.draw()

    def draw(self):
        # ins Fenster packen
        headline = tk.Label(self, text="Reisekosten/Kilometergeld")
        headline.grid(row=0, column=0, columnspan=2)

        if hasattr(self, 'jahr_dropdown'):
            self.jahr_dropdown.grid(row=0, column=5)
            self.changebutton.grid(row=0, column=6)

        u8_label = tk.Label(master=self, text="Unter 8 Stunden Abwesenheit:")
        u8_label.grid(row=1, column=0)
        self.u8.grid(row=1, column=1)

        ue8_label = tk.Label(master=self, text="Über 8 Stunden Abwesenheit:")
        ue8_label.grid(row=2, column=0)
        self.ue8.grid(row=2, column=1)

        ue24_label = tk.Label(master=self, text="Über 24 Stunden Abwesenheit:")
        ue24_label.grid(row=3, column=0)
        self.ue24.grid(row=3, column=1)

    def set_data(self, **kwargs):
        pass

    def get_data(self):
        pass
