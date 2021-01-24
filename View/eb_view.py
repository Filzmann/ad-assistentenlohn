import tkinter as tk


class EbView(tk.Frame):

    def __init__(self, parent_view, ebliste, akt_eb):
        super().__init__(parent_view)
        self.eb = akt_eb
        self.selected = tk.StringVar()
        self.selected.set(ebliste[0])
        self.eb_dropdown = tk.OptionMenu(self, self.selected, *ebliste, command=self.change_eb)
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        self.email_input = tk.Entry(self, bd=5, width=40)

        headline = tk.Label(self, text="EB auswählen")
        headline.grid(row=0, column=0)
        self.eb_dropdown.grid(row=0, column=1)
        vorname_label = tk.Label(self, text="Vorname")
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        nachname_label = tk.Label(self, text="Nachname")
        nachname_label.grid(row=2, column=0)
        self.nachname_input.grid(row=2, column=1, columnspan=2)
        email_label = tk.Label(self, text="Email")
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)

    def set_data(self, **kwargs):
        self.vorname_input.delete(0, 'end')
        self.nachname_input.delete(0, 'end')
        self.email_input.delete(0, 'end')

        self.vorname_input.insert(0, kwargs['vorname'])
        self.nachname_input.insert(0, kwargs['name'])
        self.email_input.insert(0, kwargs['email'])

    def get_data(self):
        return{'vorname': self.vorname_input.get(),
               'name': self.nachname_input.get(),
               'email': self.email_input.get()}

    def change_eb(self, eb):
        if not eb or eb == "EB wählen oder neu anlegen":
            self.set_data(vorname='', name='', email='')
            self.eb = None
        else:
            self.set_data(vorname=eb.vorname,
                          name=eb.name,
                          email=eb.email)
            self.eb = eb


