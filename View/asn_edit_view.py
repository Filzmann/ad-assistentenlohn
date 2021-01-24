import tkinter as tk

from Controller.eb_controller import EbController
from Controller.pfk_controller import PfkController


class AsnAuswahllisteFrame(tk.Frame):

    def __init__(self, parent_view, asn_liste, selected_asn_id):
        super().__init__(parent_view)
        self.parent_view = parent_view
        self.selected_asn = tk.IntVar()
        self.selected_asn.set(selected_asn_id)

        for asn in asn_liste:
            button = tk.Radiobutton(self,
                                    text=asn["kuerzel"],
                                    padx=20,
                                    variable=self.selected_asn,
                                    value=int(asn["id"]))
            button.pack()


class AsnEditorFrame(tk.Frame):
    eb: EbController = None
    pfk: PfkController = None

    def __init__(self, parent_view, selected_asn):
        super().__init__(parent_view)
        self.stammdaten = tk.Label(self, text="Stammdaten")
        self.feste_schichten = tk.Label(self, text="feste Schichten")
        self.templates = tk.Label(self, text="Templates")
        self.save_button = tk.Button(self, text="ASN speichern")
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)

        self.draw()

    def draw(self):
        self.stammdaten.grid(row=0, column=0, rowspan=2)
        if self.eb:
            self.eb.grid(row=0, column=1)
        if self.pfk:
            self.pfk.grid(row=1, column=1)
        self.save_button.grid(row=2, column=0)
        self.exit_button.grid(row=2, column=1)
        self.feste_schichten.grid(row=3, column=0)
        self.templates.grid(row=3, column=1)


class AsnEditView(tk.Toplevel):
    choose: AsnAuswahllisteFrame = None
    edit: AsnEditorFrame = None

    def __init__(self, parent_view,
                 asn_liste: list = None,
                 selected_asn_id=999999999):
        if not asn_liste:
            asn_liste = [{'id': 999999999, 'kuerzel': 'Neuer ASN'}]
        else:
            asn_liste.append({'id': 999999999, 'kuerzel': 'Neuer ASN'})
        super().__init__(parent_view)
        self.asn_liste = asn_liste
        self.selected_asn_id = selected_asn_id
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
                                           selected_asn_id=self.selected_asn_id)
        self.choose.grid(row=0, column=0)
        self.edit = AsnEditorFrame(parent_view=self,
                                   selected_asn=self.selected_asn_id)
        self.edit.grid(row=0, column=1)
