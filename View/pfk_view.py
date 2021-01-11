import tkinter as tk


class PfkView(tk.Frame):
    def __init__(self, parent_view, ebliste=["PFK wählen oder neu anlegen"]):
        super().__init__(parent_view)
        headline = tk.Label(self, text="PFK auswählen")
        self.selected = tk.StringVar()
        self.selected.set(ebliste[0])
        self.pfk_dropdown = tk.OptionMenu(self, self.selected, *ebliste)

        vorname_label = tk.Label(self, text="Vorname")
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        nachname_label = tk.Label(self, text="Nachname")
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        email_label = tk.Label(self, text="Email")
        self.email_input = tk.Entry(self, bd=5, width=40)

        headline.grid(row=0, column=0)
        self.pfk_dropdown.grid(row=0, column=1)
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        nachname_label.grid(row=2, column=0)
        self.nachname_input.grid(row=2, column=1, columnspan=2)
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)

    def set_data(self, **kwargs):
        self.vorname_input.insert(0, kwargs['vorname'])
        self.nachname_input.insert(0, kwargs['name'])
        self.email_input.insert(0, kwargs['email'])

    def get_data(self):
        return{'vorname': self.vorname_input.get(),
               'nachname': self.nachname_input.get(),
               'email': self.email_input.get()}
