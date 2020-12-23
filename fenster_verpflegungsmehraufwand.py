import tkinter as tk
import datetime

from person import AS, Adresse


class FensterVerpflegungsMehraufwand(tk.Toplevel):
    class TabelleVerpflegungsMehraufwand(tk.Frame):
        def __init__(self, parent, assistent: AS, jahr: tk.IntVar):
            super().__init__(parent)
            self.alle_unklarheiten_beseitigt = True
            self.assistent = assistent
            self.jahr = jahr.get()
            self.entry_input_minuten = None
            self.entry_input_km = None
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
                if not schichten[schicht].ist_ausfallgeld:
                    beginnadresse = endadresse = schichten[schicht].asn.home
                    if schichten[schicht].beginn_andere_adresse:
                        beginnadresse = schichten[schicht].beginn_andere_adresse
                    if schichten[schicht].ende_andere_adresse:
                        endadresse = schichten[schicht].ende_andere_adresse
                    abwesenheit = schichten[schicht].ende - schichten[schicht].beginn
                    zeit_hinfahrt = self.assistent.get_fahrtzeit(self.assistent.home, beginnadresse)
                    if not zeit_hinfahrt:
                        self.alle_unklarheiten_beseitigt = False
                        self.ask_wegzeit(self.assistent.home,
                                         beginnadresse,
                                         asn=schichten[schicht].asn.kuerzel)
                    abwesenheit += datetime.timedelta(minutes=zeit_hinfahrt)
                    zeit_rueckfahrt = self.assistent.get_fahrtzeit(self.assistent.home, endadresse)
                    if not zeit_rueckfahrt:
                        self.alle_unklarheiten_beseitigt = False
                        self.ask_wegzeit(self.assistent.home,
                                         endadresse,
                                         asn=schichten[schicht].asn.kuerzel)
                    if not self.alle_unklarheiten_beseitigt:
                        break
                    if self.alle_unklarheiten_beseitigt:
                        abwesenheit += datetime.timedelta(minutes=zeit_rueckfahrt)
                        abwesenheit_stunden = abwesenheit.days * 24 + abwesenheit.seconds / 3600
                        if abwesenheit_stunden > 24:
                            if schichten[schicht].teilschichten:
                                for teilschicht in schichten[schicht].teilschichten:
                                    differenz = (teilschicht.ende - teilschicht.beginn).days * 24 + (
                                            teilschicht.ende - teilschicht.beginn).seconds / 3600
                                    if differenz == 24:
                                        steuerarray['Abwesenheit über 24 Stunden'] += 1
                                    else:
                                        steuerarray['An-/Abreisetag'] += 1
                            else:
                                steuerarray['Abwesenheit über 24 Stunden'] += 1
                        elif abwesenheit.seconds / 3600 > 8:
                            steuerarray['Abwesenheit über 8 Stunden'] += 1
                        else:
                            steuerarray['Abwesenheit unter 8 Stunden'] += 1

            if self.alle_unklarheiten_beseitigt:
                zeilennummer = 4
                for zeile in steuerarray:
                    label = tk.Label(self, text=zeile)
                    label.grid(row=zeilennummer, column=0, sticky="w")
                    entry = tk.Label(self, text=steuerarray[zeile])
                    entry.grid(row=zeilennummer, column=1, sticky="e")
                    zeilennummer += 1
                    self.grid()

        def ask_wegzeit(self, adresse1: Adresse, adresse2: Adresse, asn):
            if adresse1 == self.assistent.home:
                string_adresse1 = "Dein zu Hause, " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            else:
                string_adresse1 = asn + ", " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            if adresse2 == self.assistent.home:
                string_adresse2 = "Dein zu Hause, " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            else:
                string_adresse2 = asn + ", " + adresse2.strasse + " " + \
                                  adresse2.hnr + ", " + adresse2.plz + " " + adresse2.stadt + "\n"

            text1 = "Wieviele Minuten(!) benötigst du normalerweise \n" \
                    "für die Strecke von \n" + string_adresse1 + \
                    " nach \n" + string_adresse2 + "?"
            text2 = "Wieviele Kilometer sind das? \n" \
                    "Leider kann ich google Maps (noch) nicht selber fragen \n" + \
                    "Aber ich frage für jede Strecke auch nur einmal. Versprochen!"
            label_input_minuten = tk.Label(self, text=text1)
            self.entry_input_minuten = tk.Entry(self, width=10)
            labelinput_km = tk.Label(self, text=text2)
            self.entry_input_km = tk.Entry(self, width=10)
            submit = tk.Button(self, text="Speichern", command=self.weg_speichern)

            label_input_minuten.grid(row=0, column=0)
            self.entry_input_minuten.grid(row=1, column=0)
            labelinput_km.grid(row=2, column=0)
            self.entry_input_km.grid(row=3, column=0)
            submit.grid(row=4, column=0)

        def weg_speichern(self):
            pass

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
