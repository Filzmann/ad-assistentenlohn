import tkinter as tk


class AsnEditView(tk.Toplevel):
    def __init__(self, parent_view,
                 asn_liste: list,
                 selected_asn_id=-1):
        super().__init__(parent_view)

        # linke Seite - Liste
        self.choose = tk.Frame(self)
        self.asn_liste = asn_liste
        self.selected_asn = tk.IntVar()
        self.selected_asn.set(selected_asn_id)

        for asn in asn_liste:
            button = tk.Radiobutton(self.choose,
                                    text=asn["kuerzel"],
                                    padx=20,
                                    variable=self.selected_asn,
                                    value=int(asn["id"]))
            button.pack()
        self.selected_asn_id = selected_asn_id

        # rechte seite - Formular
        self.edit = tk.Frame(master=self)
        self.edit.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        self.stammdaten = tk.Label(self.edit, text="Stammi")  # tk.Frame(master=self.edit)
        self.eb = tk.Frame(master=self.edit)
        self.pfk = tk.Frame(master=self.edit)

        self.save_button = tk.Button(self, text="ASN speichern")
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)

        self.feste_schichten = tk.Frame(master=self.edit)
        self.templates = tk.Frame(master=self.edit)

        self.title('Assistenznehmer bearbeiten')

        self.draw()

    def draw(self):
        self.choose.grid(row=0, column=0)

        self.edit.grid(row=0, column=1)

        self.stammdaten.grid(row=0, column=0, rowspan=2)
        if self.eb:
            self.eb.grid(row=0, column=1)
        if self.pfk:
            self.pfk.grid(row=1, column=1)

        self.save_button.grid(row=2, column=0)
        self.exit_button.grid(row=2, column=1)

        self.feste_schichten.grid(row=3, column=0)
        self.templates.grid(row=3, column=1)
