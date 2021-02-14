import tkinter as tk


class SummenView(tk.Frame):
    def __init__(self, parent_view, data):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        self.draw(data)

    def draw(self, data):
        for child in self.winfo_children():
            child.destroy()

        zeile=0
        # Kopfzeile
        bezeichner_kopf = tk.Label(master=self, text="Bezeichnung")
        anzahl_kopf = tk.Label(master=self, text="Anzahl")
        wert_kopf = tk.Label(master=self, text="Pro Stunde")
        gesamt_kopf = tk.Label(master=self, text="Gesamt")

        bezeichner_kopf.grid(row=zeile, column=0, sticky=tk.NW)
        anzahl_kopf.grid(row=zeile, column=1, sticky=tk.NE)
        wert_kopf.grid(row=zeile, column=2, sticky=tk.NE)
        gesamt_kopf.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1

        bezeichner_grund = tk.Label(master=self, text="Grundlohn")
        anzahl_grund = tk.Label(master=self, text="{:,.2f}".format(data['arbeitsstunden']))
        wert_grund = tk.Label(master=self, text="{:,.2f}€".format(data['stundenlohn']))
        gesamt_grund = tk.Label(master=self, text="{:,.2f}€".format(data['lohn']))

        bezeichner_grund.grid(row=zeile, column=0, sticky=tk.NW)
        anzahl_grund.grid(row=zeile, column=1, sticky=tk.NE)
        wert_grund.grid(row=zeile, column=2, sticky=tk.NE)
        gesamt_grund.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1

        if data['bsd_stunden']:
            bezeichner_bsd = tk.Label(master=self, text="Zuschlag kurzfr. Vermittlung")
            anzahl_bsd = tk.Label(master=self, text="{:,.2f}".format(data['bsd_stunden']))
            wert_bsd = tk.Label(master=self, text="{:,.2f}€".format(data['bsd'] * 0.2))
            gesamt_bsd = tk.Label(master=self, text="{:,.2f}€".format(data['bsd_kumuliert']))
    
            bezeichner_bsd.grid(row=3, column=0, sticky=tk.NW)
            anzahl_bsd.grid(row=3, column=1, sticky=tk.NE)
            wert_bsd.grid(row=3, column=2, sticky=tk.NE)
            gesamt_bsd.grid(row=3, column=3, sticky=tk.NE)
            zeile += 1

        if data['nachtstunden']:
            bezeichner_nacht = tk.Label(master=self, text="Nachtzuschläge")
            anzahl_nacht = tk.Label(master=self, text="{:,.2f}".format(data['nachtstunden']))
            wert_nacht = tk.Label(master=self, text="{:,.2f}€".format(data['nachtzuschlag']))
            gesamt_nacht = tk.Label(master=self, text="{:,.2f}€".format(data['nachtzuschlag_kumuliert']))
    
            bezeichner_nacht.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_nacht.grid(row=zeile, column=1, sticky=tk.NE)
            wert_nacht.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_nacht.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1

        bezeichner_orga = tk.Label(master=self, text="Organisationszuschlag")
        anzahl_orga = tk.Label(master=self, text="{:,.2f}".format(data['arbeitsstunden']))
        wert_orga = tk.Label(master=self, text="{:,.2f}€".format(data['orga_zuschlag']))
        gesamt_orga = tk.Label(master=self, text="{:,.2f}€".format(data['orga_zuschlag_kumuliert']))

        bezeichner_orga.grid(row=zeile, column=0, sticky=tk.NW)
        anzahl_orga.grid(row=zeile, column=1, sticky=tk.NE)
        wert_orga.grid(row=zeile, column=2, sticky=tk.NE)
        gesamt_orga.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1

        bezeichner_wechselschicht = tk.Label(master=self, text="Wechselschichtzuschlag")
        anzahl_wechselschicht = tk.Label(master=self, text="{:,.2f}".format(data['arbeitsstunden']))
        wert_wechselschicht = tk.Label(master=self, text="{:,.2f}€".format(data['wechselschicht_zuschlag']))
        gesamt_wechselschicht = tk.Label(master=self, text="{:,.2f}€".format(data['wechselschicht_zuschlag_kumuliert']))

        bezeichner_wechselschicht.grid(row=zeile, column=0, sticky=tk.NW)
        anzahl_wechselschicht.grid(row=zeile, column=1, sticky=tk.NE)
        wert_wechselschicht.grid(row=zeile, column=2, sticky=tk.NE)
        gesamt_wechselschicht.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1



        # bruttolohn
        bezeichner_bruttolohn = tk.Label(master=self, text="Bruttolohn")
        gesamt_bruttolohn = tk.Label(master=self, text="{:,.2f}€".format(data['bruttolohn']))

        bezeichner_bruttolohn.grid(row=zeile, column=0, sticky=tk.NW)
        gesamt_bruttolohn.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1
