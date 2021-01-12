import tkinter as tk


class RegelmaessigeSchichtenView(tk.Frame):

    def __init__(self, parent_view):
        super().__init__(parent_view)
        kuerzel_label = tk.Label(self, text="Kürzel")
        self.kuerzel_input = tk.Entry(self, bd=5, width=40)
        vorname_label = tk.Label(self, text="Vorname")
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        nachname_label = tk.Label(self, text="Nachname")
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        email_label = tk.Label(self, text="Email")
        self.email_input = tk.Entry(self, bd=5, width=40)
        strasse_label = tk.Label(self, text="Straße/Hausnummer")
        self.strasse_input = tk.Entry(self, bd=5, width=29)
        self.hausnummer_input = tk.Entry(self, bd=5, width=9)
        plz_label = tk.Label(self, text="Postleitzahl")
        self.plz_input = tk.Entry(self, bd=5, width=40)
        stadt_label = tk.Label(self, text="Stadt")
        self.stadt_input = tk.Entry(self, bd=5, width=40)
        buero_label = tk.Label(self, text="Zuständiges Einsatzbüro")
        # TODO in Klassen überführen
        option_list = ['Bitte auswählen', 'Nordost', 'West', 'Süd']
        self.selected_buero = tk.StringVar()
        self.selected_buero.set(option_list[0])
        self.buero_dropdown = tk.OptionMenu(self, self.selected_buero, *option_list)

        # positionieren
        kuerzel_label.grid(row=0, column=0)
        self.kuerzel_input.grid(row=0, column=1, columnspan=2)
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        nachname_label.grid(row=2, column=0)
        self.nachname_input.grid(row=2, column=1, columnspan=2)
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)
        strasse_label.grid(row=4, column=0)
        self.strasse_input.grid(row=4, column=1)
        self.hausnummer_input.grid(row=4, column=2)
        plz_label.grid(row=5, column=0)
        self.plz_input.grid(row=5, column=1, columnspan=2)
        stadt_label.grid(row=6, column=0)
        self.stadt_input.grid(row=6, column=1, columnspan=2)
        buero_label.grid(row=7, column=0)
        self.buero_dropdown.grid(row=7, column=1)

    def set_data(self, **kwargs):
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
        return{'kuerzel': self.kuerzel_input.get(),
               'vorname': self.vorname_input.get(),
               'nachname': self.nachname_input.get(),
               'email': self.email_input.get(),
               'strasse': self.strasse_input.get(),
               'hnr': self.hausnummer_input.get(),
               'plz': self.plz_input.get(),
               'stadt': self.stadt_input.get(),
               'buero': self.selected_buero.get()}
