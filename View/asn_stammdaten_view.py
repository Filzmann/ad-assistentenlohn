import tkinter as tk


class AsnStammdatenView(tk.Frame):

    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.config(
            highlightbackground="green",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        self.kuerzel_input = tk.Entry(self, bd=5, width=40)
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        self.email_input = tk.Entry(self, bd=5, width=40)
        self.strasse_input = tk.Entry(self, bd=5, width=29)
        self.hausnummer_input = tk.Entry(self, bd=5, width=9)
        self.plz_input = tk.Entry(self, bd=5, width=40)
        self.stadt_input = tk.Entry(self, bd=5, width=40)
        option_list = ['Bitte auswählen', 'Nordost', 'West', 'Süd']
        self.selected_buero = tk.StringVar()
        self.selected_buero.set(option_list[0])
        self.buero_dropdown = tk.OptionMenu(self, self.selected_buero, *option_list)

        self.draw()

    def draw(self):
        # positionieren
        kuerzel_label = tk.Label(self, text="Kürzel* ")
        kuerzel_label.grid(row=0, column=0, sticky=tk.NW)
        self.kuerzel_input.grid(row=0, column=1, columnspan=2, sticky=tk.NW)
        vorname_label = tk.Label(self, text="Vorname")
        vorname_label.grid(row=1, column=0, sticky=tk.NW)
        self.vorname_input.grid(row=1, column=1, columnspan=2, sticky=tk.NW)
        nachname_label = tk.Label(self, text="Nachname")
        nachname_label.grid(row=2, column=0, sticky=tk.NW)
        self.nachname_input.grid(row=2, column=1, columnspan=2, sticky=tk.NW)
        email_label = tk.Label(self, text="Email")
        email_label.grid(row=3, column=0, sticky=tk.NW)
        self.email_input.grid(row=3, column=1, columnspan=2, sticky=tk.NW)
        strasse_label = tk.Label(self, text="Straße/Hausnummer")
        strasse_label.grid(row=4, column=0, sticky=tk.NW)
        self.strasse_input.grid(row=4, column=1, sticky=tk.NW)
        self.hausnummer_input.grid(row=4, column=2, sticky=tk.NW)
        plz_label = tk.Label(self, text="Postleitzahl")
        plz_label.grid(row=5, column=0, sticky=tk.NW)
        self.plz_input.grid(row=5, column=1, columnspan=2, sticky=tk.NW)
        stadt_label = tk.Label(self, text="Stadt")
        stadt_label.grid(row=6, column=0, sticky=tk.NW)
        self.stadt_input.grid(row=6, column=1, columnspan=2, sticky=tk.NW)
        buero_label = tk.Label(self, text="Zuständiges Einsatzbüro")
        buero_label.grid(row=7, column=0, sticky=tk.NW)
        self.buero_dropdown.grid(row=7, column=1, sticky=tk.NW)

    def set_data(self, **kwargs):
        # alle Felder leeren

        self.kuerzel_input.delete(0, "end")
        self.vorname_input.delete(0, "end")
        self.nachname_input.delete(0, "end")
        self.email_input.delete(0, "end")
        self.strasse_input.delete(0, "end")
        self.hausnummer_input.delete(0, "end")
        self.plz_input.delete(0, "end")
        self.stadt_input.delete(0, "end")

        # und neu befüllen
        self.kuerzel_input.insert(0, kwargs['kuerzel'])
        self.vorname_input.insert(0, kwargs['vorname'])
        self.nachname_input.insert(0, kwargs['name'])
        self.email_input.insert(0, kwargs['email'])
        self.strasse_input.insert(0, kwargs['strasse'])
        self.hausnummer_input.insert(0, kwargs['hnr'])
        self.plz_input.insert(0, kwargs['plz'])
        self.stadt_input.insert(0, kwargs['stadt'])
        self.selected_buero.set(kwargs['buero'])

    def get_data(self):
        return {'kuerzel': self.kuerzel_input.get(),
                'vorname': self.vorname_input.get(),
                'nachname': self.nachname_input.get(),
                'email': self.email_input.get(),
                'strasse': self.strasse_input.get(),
                'hnr': self.hausnummer_input.get(),
                'plz': self.plz_input.get(),
                'stadt': self.stadt_input.get(),
                'buero': self.selected_buero.get()}
