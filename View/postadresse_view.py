import tkinter as tk


class PostadresseView(tk.Frame):

    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.kuerzel_label = tk.Label(self, text="Kürzel")
        self.kuerzel_input = tk.Entry(self, bd=5, width=40)
        self.strasse_label = tk.Label(self, text="Straße/Hausnummer")
        self.strasse_input = tk.Entry(self, bd=5, width=29)
        self.hausnummer_input = tk.Entry(self, bd=5, width=9)
        self.plz_label = tk.Label(self, text="Postleitzahl")
        self.plz_input = tk.Entry(self, bd=5, width=40)
        self.stadt_label = tk.Label(self, text="Stadt")
        self.stadt_input = tk.Entry(self, bd=5, width=40)
        self.draw()

    def draw(self):
        # positionieren
        self.kuerzel_label.grid(row=0, column=0, sticky=tk.NW)
        self.kuerzel_input.grid(row=0, column=1, columnspan=2, sticky=tk.NW)
        self.strasse_label.grid(row=4, column=0, sticky=tk.NW)
        self.strasse_input.grid(row=4, column=1, sticky=tk.NW)
        self.hausnummer_input.grid(row=4, column=2, sticky=tk.NW)
        self.plz_label.grid(row=5, column=0, sticky=tk.NW)
        self.plz_input.grid(row=5, column=1, columnspan=2, sticky=tk.NW)
        self.stadt_label.grid(row=6, column=0, sticky=tk.NW)
        self.stadt_input.grid(row=6, column=1, columnspan=2, sticky=tk.NW)

    def set_data(self, **kwargs):
        # alle Felder leeren

        self.kuerzel_input.delete(0, "end")
        self.strasse_input.delete(0, "end")
        self.hausnummer_input.delete(0, "end")
        self.plz_input.delete(0, "end")
        self.stadt_input.delete(0, "end")

        # und neu befüllen
        self.kuerzel_input.insert(0, kwargs['kuerzel'])
        self.strasse_input.insert(0, kwargs['strasse'])
        self.hausnummer_input.insert(0, kwargs['hnr'])
        self.plz_input.insert(0, kwargs['plz'])
        self.stadt_input.insert(0, kwargs['stadt'])

    def get_data(self):
        return{'kuerzel': self.kuerzel_input.get(),
               'strasse': self.strasse_input.get(),
               'hnr': self.hausnummer_input.get(),
               'plz': self.plz_input.get(),
               'stadt': self.stadt_input.get(),
               }
