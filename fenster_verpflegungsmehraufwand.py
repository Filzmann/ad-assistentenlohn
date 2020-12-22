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
            steuerarray = {"über 24":0, "über 8": 0, "unter 8": 0}
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
                if abwesenheit.hours > 24:
                    steuerarray['über 24'] += 1
                elif abwesenheit.hours > 8:
                    steuerarray['über 8'] += 1
                else:
                    steuerarray['unter 8'] += 1

            zeilennummer = 0
            for zeile in steuerarray:
                label = tk.Label(self, text =zeile)
                label.grid(row=zeilennummer, column=0)
                label = tk.Label(self, text=steuerarray[zeile])
                label.grid(row=zeilennummer, column=1)
                zeilennummer += 1


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
