import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar

from Helpers.combobox_dict import Combobox


class AskholeView(tk.Toplevel):
    def __init__(self, parent_view, **kwargs):
        super().__init__(parent_view)
        self.parent = parent_view
        self.km = tk.Entry(self, width=5)
        self.min = tk.Entry(self, width=5)
        self.button = tk.Button(self, text="Speichern")
        self.kwargs = kwargs

        self.draw()

    def draw(self):
        # ins Fenster packen
        headline = tk.Label(self, text="Verpflegungsmehraufwand")
        headline.grid(row=0, column=0, columnspan=2)

        text= "Leider kann ich selber (noch) nicht googeln. \n" \
              "Daher bitte ich um die Beantwortung folgender wichtigen Frage:\n" \
              "(ich frage dich auch für jeden Weg nur 1 mal, versprochen) \n \n" \
              "Wieviele Minuten brauchst du von \n"
        text += str(self.kwargs['adresse1']) + " \n nach \n"
        text += str(self.kwargs['adresse2']) + "?"
        textfeld = tk.Label(self, text=text)
        textfeld.grid(row=1, column=0, columnspan=2)

        label_km = tk.Label(self, text="Kilometer:")
        label_km.grid(row=2, column=0)
        self.km.grid(row=2, column=1)

        label_min = tk.Label(self, text="Minuten:")
        label_min.grid(row=3, column=0)
        self.min.grid(row=3, column=1)

    def set_data(self, **kwargs):
        pass

    def get_data(self):
        pass
