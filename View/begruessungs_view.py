import tkinter as tk


class BegruessungsView(tk.Frame):
    def __init__(self, parent, assistentenliste=None):
        super().__init__(parent)
        self.parent = parent
        if assistentenliste:
            self.selected = tk.StringVar()
            self.selected.set(assistentenliste[0])
            self.dropdown = tk.OptionMenu(self, self.selected, *assistentenliste)
            self.button_oeffnen = tk.Button(self, text="Gespeicherten Assistenten laden")

        self.info_text = tk.Label(self, text="Bitte erstelle oder öffne eine_n Assistent_in")
        self.button_neu = tk.Button(self, text="Neuen Assistenten anlegen")

        self.info_text.grid(row=0, column=0, columnspan=2, sticky="e")
        if assistentenliste:
            self.dropdown.grid(row=1, column=0)
            self.button_oeffnen.grid(row=1, column=1, sticky="e")
        self.button_neu.grid(row=1, column=2, sticky="e")

    def get_selected(self):
        return self.selected.get()
