import tkinter as tk

from tkcalendar import Calendar

from Model.schicht import Schicht
from Helpers.combobox_dict import Combobox
from View.asn_stammdaten_view import AsnStammdatenView
from View.postadresse_view import PostadresseView
from timepicker import TimePicker


class SchichtView(tk.Toplevel):
    def __init__(self, parent_view, asn_liste, adressliste, schicht: Schicht = None):
        super().__init__(parent_view)

        self.asn_dropdown = Combobox(self, values=asn_liste, width=38, state="readonly")
        self.asn_dropdown.set("-1")

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

        self.abweichende_adresse_beginn_dropdown = Combobox(self, values=adressliste, width=38, state="readonly")
        self.abweichende_adresse_beginn_dropdown.set("-1")
        self.abweichende_adresse_ende_dropdown = Combobox(self, values=adressliste, width=38, state="readonly")
        self.abweichende_adresse_ende_dropdown.set("-1")

        self.ist_at_button = tk.Checkbutton(self, text="AT",  onvalue=1, offvalue=0)
        self.ist_pcg_button = tk.Checkbutton(self, text="PCG", onvalue=1, offvalue=0)
        self.ist_rb_button = tk.Checkbutton(self, text="Kurzfristig (RB/BSD)", onvalue=1,
                                            offvalue=0)
        self.ist_afg_button = tk.Checkbutton(self, text="Ausfallgeld", onvalue=1, offvalue=0)

        self.draw()

    def draw(self):
        asn_label = tk.Label(self, text='ASN auswählen')

        asn_label.grid(row=0, column=0, sticky=tk.NW)
        self.asn_dropdown.grid(row=0, column=1, sticky=tk.NE)

        self.asn_stammdaten_form.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

        startdatum_label = tk.Label(self, text='Start')
        startdatum_label.grid(row=0, column=3, sticky=tk.NW)
        self.startdatum_input.grid(row=1, column=3, sticky=tk.NW, columnspan=2)
        self.startzeit_input.grid(row=0, column=4, sticky=tk.NW)

        enddatum_label = tk.Label(self, text='End')
        enddatum_label.grid(row=0, column=5, sticky=tk.NW)
        self.enddatum_input.grid(row=1, column=5, sticky=tk.NW, columnspan=2)
        self.endzeit_input.grid(row=0, column=6, sticky=tk.NW)

        self.abweichende_adresse_beginn_dropdown.grid(row=3, column=0, sticky=tk.NW)
        self.abweichende_adresse_beginn.grid(row=3, column=1, sticky=tk.NW)
        self.abweichende_adresse_ende_dropdown.grid(row=4, column=0, sticky=tk.NW)
        self.abweichende_adresse_ende.grid(row=4, column=1, sticky=tk.NW)

        self.ist_at_button.grid(row=5, column=1, sticky=tk.NW)
        self.ist_pcg_button.grid(row=6, column=1, sticky=tk.NW)
        self.ist_rb_button.grid(row=7, column=1, sticky=tk.NW)
        self.ist_afg_button.grid(row=8, column=1, sticky=tk.NW)

