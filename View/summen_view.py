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

        zeile = 0
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

        if data['urlaubsstunden']:
            bezeichner_grund = tk.Label(master=self, text="Entgelt Urlaub")
            anzahl_grund = tk.Label(master=self, text="{:,.2f}".format(data['urlaubsstunden']))
            wert_grund = tk.Label(master=self, text="{:,.2f}€".format(data['stundenlohn_urlaub']))
            gesamt_grund = tk.Label(master=self, text="{:,.2f}€".format(data['urlaubslohn']))

            bezeichner_grund.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_grund.grid(row=zeile, column=1, sticky=tk.NE)
            wert_grund.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_grund.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1

        if data['austunden']:
            bezeichner_grund = tk.Label(master=self, text="Entgelt Arbeitsunfähigkeit")
            anzahl_grund = tk.Label(master=self, text="{:,.2f}".format(data['austunden']))
            wert_grund = tk.Label(master=self, text="{:,.2f}€".format(data['stundenlohn_au']))
            gesamt_grund = tk.Label(master=self, text="{:,.2f}€".format(data['aulohn']))

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

        if 'samstag_zuschlag_bezeichner' in data:
            bezeichner_samstag_zuschlag = tk.Label(master=self, text="Zuschlag Samstag")
            anzahl_samstag_zuschlag = tk.Label(master=self, text="{:,.2f}".format(data['samstag_zuschlag_stunden']))
            wert_samstag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['samstag_zuschlag_pro_stunde']))
            gesamt_samstag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['samstag_zuschlag_kumuliert']))

            bezeichner_samstag_zuschlag.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_samstag_zuschlag.grid(row=zeile, column=1, sticky=tk.NE)
            wert_samstag_zuschlag.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_samstag_zuschlag.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1
        
        if 'sonntag_zuschlag_bezeichner' in data:
            bezeichner_sonntag_zuschlag = tk.Label(master=self, text="Zuschlag Sonntag")
            anzahl_sonntag_zuschlag = tk.Label(master=self, text="{:,.2f}".format(data['sonntag_zuschlag_stunden']))
            wert_sonntag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['sonntag_zuschlag_pro_stunde']))
            gesamt_sonntag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['sonntag_zuschlag_kumuliert']))

            bezeichner_sonntag_zuschlag.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_sonntag_zuschlag.grid(row=zeile, column=1, sticky=tk.NE)
            wert_sonntag_zuschlag.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_sonntag_zuschlag.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1
            
        if 'feiertag_zuschlag_bezeichner' in data:
            bezeichner_feiertag_zuschlag = tk.Label(master=self, text="Zuschlag Feiertag")
            anzahl_feiertag_zuschlag = tk.Label(master=self, text="{:,.2f}".format(data['feiertag_zuschlag_stunden']))
            wert_feiertag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['feiertag_zuschlag_pro_stunde']))
            gesamt_feiertag_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['feiertag_zuschlag_kumuliert']))

            bezeichner_feiertag_zuschlag.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_feiertag_zuschlag.grid(row=zeile, column=1, sticky=tk.NE)
            wert_feiertag_zuschlag.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_feiertag_zuschlag.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1

        if 'hl_abend_zuschlag_bezeichner' in data:
            bezeichner_hl_abend_zuschlag = tk.Label(master=self, text="Zuschlag Hl.Abend")
            anzahl_hl_abend_zuschlag = tk.Label(master=self, text="{:,.2f}".format(data['hl_abend_zuschlag_stunden']))
            wert_hl_abend_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['hl_abend_zuschlag_pro_stunde']))
            gesamt_hl_abend_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['hl_abend_zuschlag_kumuliert']))

            bezeichner_hl_abend_zuschlag.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_hl_abend_zuschlag.grid(row=zeile, column=1, sticky=tk.NE)
            wert_hl_abend_zuschlag.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_hl_abend_zuschlag.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1
            
        if 'silvester_zuschlag_bezeichner' in data:
            bezeichner_silvester_zuschlag = tk.Label(master=self, text="Zuschlag Silvester")
            anzahl_silvester_zuschlag = tk.Label(master=self, text="{:,.2f}".format(data['silvester_zuschlag_stunden']))
            wert_silvester_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['silvester_zuschlag_pro_stunde']))
            gesamt_silvester_zuschlag = tk.Label(master=self, text="{:,.2f}€".format(data['silvester_zuschlag_kumuliert']))

            bezeichner_silvester_zuschlag.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_silvester_zuschlag.grid(row=zeile, column=1, sticky=tk.NE)
            wert_silvester_zuschlag.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_silvester_zuschlag.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1

        if data['anzahl_feiertage']:
            bezeichner_freizeitausgleich = tk.Label(master=self, text="Freizeitausgleich")
            anzahl_freizeitausgleich = tk.Label(master=self, text="{:,.2f}".format(data['anzahl_feiertage']))
            wert_freizeitausgleich = tk.Label(master=self, text="Feiertage =")
            gesamt_freizeitausgleich = tk.Label(master=self, text="{:,.2f}€".format(data['freizeitausgleich']))

            bezeichner_freizeitausgleich.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_freizeitausgleich.grid(row=zeile, column=1, sticky=tk.NE)
            wert_freizeitausgleich.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_freizeitausgleich.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1
            
        if 'ueberstunden' in data:
            bezeichner_ueberstunden = tk.Label(master=self, text="Überstundenzuschlag")
            anzahl_ueberstunden = tk.Label(master=self, text="{:,.2f}".format(data['ueberstunden']))
            wert_ueberstunden = tk.Label(master=self, text="{:,.2f}€".format(data['ueberstunden_pro_stunde']))
            gesamt_ueberstunden = tk.Label(master=self, text="{:,.2f}€".format(data['ueberstunden_kumuliert']))

            bezeichner_ueberstunden.grid(row=zeile, column=0, sticky=tk.NW)
            anzahl_ueberstunden.grid(row=zeile, column=1, sticky=tk.NE)
            wert_ueberstunden.grid(row=zeile, column=2, sticky=tk.NE)
            gesamt_ueberstunden.grid(row=zeile, column=3, sticky=tk.NE)
            zeile += 1



        # bruttolohn
        bezeichner_bruttolohn = tk.Label(master=self, text="Bruttolohn")
        gesamt_bruttolohn = tk.Label(master=self, text="{:,.2f}€".format(data['bruttolohn']))

        bezeichner_bruttolohn.grid(row=zeile, column=0, sticky=tk.NW)
        gesamt_bruttolohn.grid(row=zeile, column=3, sticky=tk.NE)
        zeile += 1

        # freie Sontage
        text = 'Es gibt laut aktueller Planung noch ' + data['freie_sonntage'] + ' Sonntage, \n' \
               'an denen du arbeiten könntest.\n'
        text += 'Davon "darfst" du noch ' + data['moegliche_arbeitssonntage'] + ' Sonntage arbeiten.\n'
        text += '(Du musst jedes Jahr 15 freie Sonntage haben.)'
        bezeichner = tk.Label(master=self, text=text, justify=tk.LEFT)
        bezeichner.grid(row=zeile, column=0, columnspan=4, sticky=tk.NW)

        zeile += 1
