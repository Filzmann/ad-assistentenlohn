import tkinter as tk
import datetime

from person import AS, Adresse, Weg


class FensterKilometergeld(tk.Toplevel):
    class TabelleKilometergeld(tk.Frame):
        def __init__(self, parent, assistent: AS, jahr: tk.IntVar):
            super().__init__(parent)
            self.alle_unklarheiten_beseitigt = True
            self.assistent = assistent
            self.jahr = jahr.get()
            self.entry_input_minuten = None
            self.entry_input_km = None
            # self.draw()

        def draw(self):
            start = datetime.datetime(self.jahr, 1, 1)
            end = datetime.datetime(self.jahr + 1, 1, 1) - datetime.timedelta(seconds=1)
            schichten = self.assistent.get_all_schichten(start=start, end=end)
            # TODO Randschichten prüfen, ob sie in anderes Jahr gehören (größter Anteil Stunden)
            kmgeld_array = {}
            for schicht in schichten:
                if not schichten[schicht].ist_ausfallgeld:
                    beginnadresse = endadresse = schichten[schicht].asn.home
                    if schichten[schicht].beginn_andere_adresse:
                        beginnadresse = schichten[schicht].beginn_andere_adresse
                    if schichten[schicht].ende_andere_adresse:
                        endadresse = schichten[schicht].ende_andere_adresse
                    weg_hinfahrt = self.assistent.get_weg(self.assistent.home, beginnadresse)
                    if not weg_hinfahrt:
                        self.alle_unklarheiten_beseitigt = False
                        self.ask_wegzeit(self.assistent.home,
                                         beginnadresse,
                                         asn=schichten[schicht].asn.kuerzel,
                                         is_at=schichten[schicht].ist_assistententreffen,
                                         is_pcg=schichten[schicht].ist_pcg)
                    if not str(weg_hinfahrt) in kmgeld_array:
                        kmgeld_array[str(weg_hinfahrt)] = {"anzahl": 1, "km": weg_hinfahrt.entfernung_km}
                    else:
                        kmgeld_array[str(weg_hinfahrt)]["anzahl"] += 1

                    weg_rueckfahrt = self.assistent.get_weg(self.assistent.home, endadresse)
                    if not weg_rueckfahrt:
                        self.alle_unklarheiten_beseitigt = False
                        self.ask_wegzeit(self.assistent.home,
                                         beginnadresse,
                                         asn=schichten[schicht].asn.kuerzel,
                                         is_at=schichten[schicht].ist_assistententreffen,
                                         is_pcg=schichten[schicht].ist_pcg)
                    if not kmgeld_array[str(weg_hinfahrt)]:
                        kmgeld_array[str(weg_hinfahrt)] = {"anzahl": 1, "km": weg_rueckfahrt.entfernung_km}
                    else:
                        kmgeld_array[str(weg_hinfahrt)]["anzahl"] += 1

                    if not self.alle_unklarheiten_beseitigt:
                        break

            if self.alle_unklarheiten_beseitigt:
                zeilennummer = 4
                for zeile in kmgeld_array:
                    anzahl_fahrten = kmgeld_array[zeile]["anzahl"]
                    km = "{:,.1f}".format(kmgeld_array[zeile]["km"])
                    labeltext = str(anzahl_fahrten) + " Fahrten "
                    labeltext += zeile + " = " + str(anzahl_fahrten) + " * " + km + "km * 0,30€ = "

                    entrytext = "{:,.2f}€".format(anzahl_fahrten * kmgeld_array[zeile]["km"] * 0.3)

                    label = tk.Label(self, text=labeltext)
                    label.grid(row=zeilennummer, column=0, sticky="w")
                    entry = tk.Label(self, text=entrytext)
                    entry.grid(row=zeilennummer, column=1, sticky="e")
                    zeilennummer += 1
                    self.grid()

        def ask_wegzeit(self, adresse1: Adresse, adresse2: Adresse, asn, is_at=0, is_pcg=0):
            if adresse1 == self.assistent.home:
                string_adresse1 = "deinem zu Hause, " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            else:
                if is_at or is_pcg:
                    atpcg = "AT/PCG-"
                else:
                    atpcg = ''
                string_adresse1 = atpcg + asn + " - " + adresse1.kuerzel + ", " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            if adresse2 == self.assistent.home:
                string_adresse2 = "deinem zu Hause, " + adresse1.strasse + " " + \
                                  adresse1.hnr + ", " + adresse1.plz + " " + adresse1.stadt + "\n"

            else:
                if is_at or is_pcg:
                    atpcg = "AT/PCG-"
                else:
                    atpcg = ''
                string_adresse2 = atpcg + asn + " - " + adresse2.kuerzel + ", " + adresse2.strasse + " " + \
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

            submit = tk.Button(self, text="Speichern", command=lambda: self.weg_speichern(adresse1, adresse2))

            label_input_minuten.grid(row=0, column=0)
            self.entry_input_minuten.grid(row=1, column=0)
            labelinput_km.grid(row=2, column=0)
            self.entry_input_km.grid(row=3, column=0)
            submit.grid(row=4, column=0)

        def weg_speichern(self, adresse1, adresse2):
            if self.entry_input_minuten and self.entry_input_km:
                minuten = int(self.entry_input_minuten.get())
                km = float(self.entry_input_km.get().replace(',', '.'))
                # komma und Punkt als Trenner möglich, User ist König

                if minuten > 0 and km > 0:
                    weg = Weg(address1=adresse1,
                              address2=adresse2,
                              reisezeit_minuten=minuten,
                              entfernung_km=km)
                    self.assistent.wege.append(weg)
                    self.assistent.save_to_file()
                children = self.winfo_children()
                for child in children:
                    child.destroy()
                self.alle_unklarheiten_beseitigt = True
                self.draw()

    def __init__(self, parent, assistent):
        super().__init__(parent)
        self.assistent = assistent
        self.parent = parent
        self.headline = tk.Label(self, text="Kilometergeld")
        heute = datetime.datetime.now()
        start = self.assistent.einstellungsdatum
        jahre = list(range(start.year, heute.year + 1))
        self.selected_year = tk.IntVar()
        self.selected_year.set(heute.year)
        self.jahr_dropdown = tk.OptionMenu(self, self.selected_year, *jahre, command=self.change_jahr)
        self.tabelle_vma = self.TabelleKilometergeld(self, assistent, self.selected_year)
        self.change_jahr(self.selected_year.get())
        # ins Fenster packen
        self.headline.grid(row=0, column=0)
        self.jahr_dropdown.grid(row=0, column=1)
        self.tabelle_vma.grid(row=1, column=0, columnspan=2)

    def change_jahr(self, selected_year):
        self.tabelle_vma.jahr = selected_year
        self.selected_year = selected_year
        self.tabelle_vma.draw()
