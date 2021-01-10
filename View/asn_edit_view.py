import tkinter as tk


class ASNEditView(tk.Toplevel):
    choose: tk.Frame = None
    edit: tk.Frame = None

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
        self.edit = ASNEditorFrame(parent_view=self,
                                   selected_asn=self.selected_asn)
        self.edit.grid(row=0, column=1)


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


class ASNEditorFrame(tk.Frame):
    def __init__(self, parent_view, selected_asn):
        super().__init__(parent_view)
        label = tk.Label(self, text="editor")
        label.pack()
