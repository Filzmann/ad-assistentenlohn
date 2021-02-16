import tkinter as tk
from Helpers.combobox_dict import Combobox


class EbView(tk.Frame):

    def __init__(self, parent_view, ebliste, akt_eb):
        super().__init__(parent_view)
        self.eb = akt_eb
        self.selected = tk.StringVar()

        self.eb_dropdown = Combobox(self, values=ebliste, width=38, state="readonly")
        self.eb_dropdown.set(0)


        self.vorname_input = tk.Entry(self, bd=5, width=40)
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        self.email_input = tk.Entry(self, bd=5, width=40)

        headline = tk.Label(self, text="EB auswählen")
        headline.grid(row=0, column=0, sticky=tk.NW)
        self.eb_dropdown.grid(row=0, column=1, sticky=tk.NW)
        vorname_label = tk.Label(self, text="Vorname")
        vorname_label.grid(row=1, column=0, sticky=tk.NW)
        self.vorname_input.grid(row=1, column=1, columnspan=2, sticky=tk.NW)
        nachname_label = tk.Label(self, text="Nachname")
        nachname_label.grid(row=2, column=0, sticky=tk.NW)
        self.nachname_input.grid(row=2, column=1, columnspan=2, sticky=tk.NW)
        email_label = tk.Label(self, text="Email")
        email_label.grid(row=3, column=0, sticky=tk.NW)
        self.email_input.grid(row=3, column=1, columnspan=2, sticky=tk.NW)

    def set_data(self, **kwargs):
        self.vorname_input.delete(0, 'end')
        self.nachname_input.delete(0, 'end')
        self.email_input.delete(0, 'end')

        self.vorname_input.insert(0, kwargs['vorname'])
        self.nachname_input.insert(0, kwargs['name'])
        self.email_input.insert(0, kwargs['email'])
        if 'eb_id' in kwargs.keys():
            self.eb_dropdown.set(kwargs['eb_id'])

    def get_data(self):
        return{'vorname': self.vorname_input.get(),
               'name': self.nachname_input.get(),
               'email': self.email_input.get()}
