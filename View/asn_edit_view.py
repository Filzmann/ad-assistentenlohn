import tkinter as tk


class AsnAuswahllisteFrame(tk.Frame):
    def __init__(self, parent_view, asn_liste, selected_asn):
        super().__init__(parent_view)
        self.parent_view = parent_view
        self.selected_asn = tk.StringVar()
        self.selected_asn.set(selected_asn)

        for kuerzel in asn_liste:
            button = tk.Radiobutton(self,
                                    text=kuerzel,
                                    padx=20,
                                    variable=self.selected_asn,
                                    value=kuerzel)
            button.pack()


class AsnEditorFrame(tk.Frame):

    def __init__(self, parent_view, selected_asn):
        super().__init__(parent_view)
        self.stammdaten = tk.Label(self, text="Stammdaten")
        self.eb = tk.Label(self, text="EB")
        self.pfk = tk.Label(self, text="PFK")
        self.feste_schichten = tk.Label(self, text="feste Schichten")
        self.templates = tk.Label(self, text="Templates")
        self.draw()

    def draw(self):
        self.stammdaten.grid(row=0, column=0, rowspan=2)
        self.eb.grid(row=0, column=1)
        self.pfk.grid(row=1, column=1)
        self.feste_schichten.grid(row=2, column=0)
        self.templates.grid(row=2, column=1)


class AsnEditView(tk.Toplevel):
    choose: AsnAuswahllisteFrame = None
    edit: AsnEditorFrame = None

    def __init__(self, parent_view,
                 asn_liste=['Neuer ASN'],
                 selected_asn='Neuer ASN'):
        super().__init__(parent_view)
        self.asn_liste = asn_liste
        self.selected_asn = selected_asn
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        self.title('Assistenznehmer bearbeiten')

        self.draw()

    def draw(self):
        self.choose = AsnAuswahllisteFrame(parent_view=self,
                                           asn_liste=self.asn_liste,
                                           selected_asn=self.selected_asn)
        self.choose.grid(row=0, column=0)
        self.edit = AsnEditorFrame(parent_view=self,
                                   selected_asn=self.selected_asn)
        self.edit.grid(row=0, column=1)
