import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar

from Helpers.combobox_dict import Combobox


class VerpflegungsmehraufwandView(tk.Toplevel):
    def __init__(self, parent_view, **kwargs):
        super().__init__(parent_view)
        self.parent = parent_view

        if 'jahrarray' in kwargs:
            self.jahr_dropdown = Combobox(self, values=kwargs['jahrarray'], width=5, state="readonly")
            self.changebutton = tk.Button(self, text='Go!')

        self.draw()

    def draw(self):
        # ins Fenster packen
        headline = tk.Label(self, text="Verpflegungsmehraufwand")
        headline.grid(row=0, column=0, columnspan=4)

        if hasattr(self, 'jahr_dropdown'):
            self.jahr_dropdown.grid(row=0, column=5)
            self.changebutton.grid(row=0, column=6)

    def set_data(self, **kwargs):
        pass

    def get_data(self):
        pass
