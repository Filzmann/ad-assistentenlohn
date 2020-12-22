import tkinter as tk
import datetime

from person import AS


class FensterVerpflegungsMehraufwand(tk.Toplevel):
    class TabelleVerpflegungsMehraufwand(tk.Frame):
        def __init__(self, parent, assistent: AS, jahr: tk.IntVar):
            super().__init__(parent)
            self.assistent = assistent
            self.jahr = jahr
            self.draw()

        def draw(self):
            start = datetime.datetime(self.jahr.get(), 1, 1)
            end = datetime.datetime(self.jahr.get() + 1, 1, 1) - datetime.timedelta(seconds=1)
            schichten = self.assistent.get_all_schichten(start=start, end=end)
            # TODO Randschichten prüfen, ob sie in anderes Jahr gehören (größter Anteil Stunden)

            for schicht in schichten:
                beginnadresse = endadresse = schicht.asn.home
                if schicht.beginn_andere_adresse:
                    beginnadresse = schicht.beginn_andere_adresse
                if schicht.ende_andere_adresse:
                    endadresse = schicht.ende_andere_adresse

             #   if schicht.alternative_adresse_beginn

            return schichten

    def __init__(self, parent, assistent):
        super().__init__(parent)
        self.assistent = assistent
        self.parent = parent
        self.headline = tk.Label(self, text="Verpflegungsmehraufwand")
        heute = datetime.datetime.now()
        start = self.assistent.einstellungsdatum
        jahre = list(range(start.year, heute.year + 1))
        self.selected_year = tk.IntVar()
        self.selected_year.set(heute.year)
        self.jahr_dropdown = tk.OptionMenu(self, self.selected_year, *jahre, command=self.change_jahr)
        self.tabelle_vma = self.TabelleVerpflegungsMehraufwand(parent, assistent, self.selected_year)

        # ins Fenster packen
        self.headline.grid(row=0, column=0)
        self.jahr_dropdown.grid(row=0, column=1)
        self.tabelle_vma.grid(row=1, column=0, columnspan=2)

    def change_jahr(self, selected_year):
        self.tabelle_vma.jahr = selected_year
        self.selected_year = selected_year
        self.tabelle_vma.draw()
