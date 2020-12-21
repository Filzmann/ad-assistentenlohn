import tkinter as tk
from tkcalendar import Calendar
import datetime
from arbeitszeit import Arbeitsunfaehigkeit


class FensterVerpflegungsMehraufwand(tk.Toplevel):
    def __init__(self, parent, assistent):
        super().__init__(parent)
        self.assistent = assistent
        self.parent = parent
        self.headline = tk.Label(self, text="Verpflegungsmehraufwand")


        # ins Fenster packen
        self.headline.grid(row=0, column=0, columnspan=4)


