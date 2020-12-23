import tkinter as tk
import datetime

from person import AS


class FensterVerpflegungsMehraufwand(tk.Toplevel):
    class TabelleVerpflegungsMehraufwand(tk.Frame):
        def __init__(self, parent, assistent: AS, jahr: tk.IntVar):
            super().__init__(parent)
            self.assistent = assistent
            self.jahr = jahr.get()
            self.draw()

        def draw(self):
            start = datetime.datetime(self.jahr, 1, 1)
            end = datetime.datetime(self.jahr + 1, 1, 1) - datetime.timedelta(seconds=1)
            schichten = self.assistent.get_all_schichten(start=start, end=end)
            # TODO Randschichten prüfen, ob sie in anderes Jahr gehören (größter Anteil Stunden)
            steuerarray = {"Abwesenheit über 24 Stunden": 0,
                           "An-/Abreisetag": 0,
                           "Abwesenheit über 8 Stunden": 0,
                           "Abwesenheit unter 8 Stunden": 0}
            for schicht in schichten:
                beginnadresse = endadresse = schichten[schicht].asn.home
                if schichten[schicht].beginn_andere_adresse:
                    beginnadresse = schichten[schicht].beginn_andere_adresse
                if schichten[schicht].ende_andere_adresse:
                    endadresse = schichten[schicht].ende_andere_adresse
                abwesenheit = schichten[schicht].ende - schichten[schicht].beginn
                zeit_hinfahrt = self.assistent.get_fahrtzeit(self.assistent.home, beginnadresse)
                abwesenheit += datetime.timedelta(minutes=zeit_hinfahrt)
                zeit_rueckfahrt = self.assistent.get_fahrtzeit(self.assistent.home, endadresse)
                abwesenheit += datetime.timedelta(minutes=zeit_rueckfahrt)
                if abwesenheit.seconds / 3600 > 24:
                    if schicht.teilschichten:
                        for teilschicht in schicht.teilschichten:
                            if (teilschicht.ende - teilschicht.beginn).seconds / 3600 == 24:
                                steuerarray['Abwesenheit über 24 Stunden'] += 1
                            else:
                                steuerarray['An-/Abreisetag'] += 1
                    else:
                        steuerarray['Abwesenheit über 24 Stunden'] += 1
                elif abwesenheit.seconds / 3600 > 8:
                    steuerarray['Abwesenheit über 8 Stunden'] += 1
                else:
                    steuerarray['Abwesenheit unter 8 Stunden'] += 1

            zeilennummer = 0
            for zeile in steuerarray:
                label = tk.Label(self, text=zeile)
                label.grid(row=zeilennummer, column=0, sticky="w")
                entry = tk.Label(self, text=steuerarray[zeile])
                entry.grid(row=zeilennummer, column=1, sticky="e")
                zeilennummer += 1
                self.grid()

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
        self.tabelle_vma = self.TabelleVerpflegungsMehraufwand(self, assistent, self.selected_year)
        self.change_jahr(self.selected_year.get())
        # ins Fenster packen
        self.headline.grid(row=0, column=0)
        self.jahr_dropdown.grid(row=0, column=1)
        self.tabelle_vma.grid(row=1, column=0, columnspan=2)

    def change_jahr(self, selected_year):
        self.tabelle_vma.jahr = selected_year
        self.selected_year = selected_year
        self.tabelle_vma.draw()
