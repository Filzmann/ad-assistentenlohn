import tkinter as tk

from tkcalendar import Calendar

from Model.schicht import Schicht
from Helpers.combobox_dict import Combobox
from View.asn_stammdaten_view import AsnStammdatenView
from View.postadresse_view import PostadresseView
from timepicker import TimePicker


class SchichtView(tk.Toplevel):
    def __init__(self, parent_view, asn_liste, schicht: Schicht = None):
        super().__init__(parent_view)

        self.asn_dropdown = Combobox(self, values=asn_liste, width=38, state="readonly")
        self.asn_dropdown.set("0")

        self.asn_stammdaten_form = AsnStammdatenView(parent_view=self)

        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        # day=day,
        # month=month,
        # year=year)
        self.startzeit_input = TimePicker(self)

        self.endzeit_input = TimePicker(self)
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        # , day=day, month=month, year=year)

        self.abweichende_adresse_beginn = PostadresseView(self)
        self.abweichende_adresse_ende = PostadresseView(self)

        self.draw()

    def draw(self):
        asn_label = tk.Label(self, text='ASN auswählen')

        asn_label.grid(row=0, column=0, sticky=tk.NW)
        self.asn_dropdown.grid(row=0, column=1, sticky=tk.NE)

        self.asn_stammdaten_form.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

        startdatum_label = tk.Label(self, text='Start')
        startdatum_label.grid(row=0, column=3, sticky=tk.NW)
        self.startdatum_input.grid(row=1, column=3, sticky=tk.NW)

        enddatum_label = tk.Label(self, text='End')
        enddatum_label.grid(row=0, column=4, sticky=tk.NW)
        self.enddatum_input.grid(row=1, column=4, sticky=tk.NW)




