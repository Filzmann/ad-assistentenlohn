import tkinter as tk


class BegruessungsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.info_text = tk.Label(self, text="Bitte erstelle oder öffne eine Assistenten-Datei")
        self.info_text.grid(row=0, column=0, columnspan=2, sticky="e")
        self.button_oeffnen = tk.Button(self, text="Gespeicherten Assistenten laden")
        self.button_oeffnen.grid(row=1, column=0, sticky="e")
        self.button_neu = tk.Button(self, text="Neuen Assistenten anlegen")
        self.button_neu.grid(row=1, column=1, sticky="e")
