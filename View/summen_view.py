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
        # Kopfzeile
        bezeichner_kopf = tk.Label(master=self, text="Bezeichnung")
        anzahl_kopf = tk.Label(master=self, text="Anzahl")
        wert_kopf = tk.Label(master=self, text="Pro Stunde")
        gesamt_kopf = tk.Label(master=self, text="Gesamt")

        bezeichner_grund = tk.Label(master=self, text="Grundlohn")
        anzahl_grund = tk.Label(master=self, text="{:,.2f}".format(data['arbeitsstunden']))
        wert_grund = tk.Label(master=self, text="{:,.2f}€".format(data['stundenlohn']))
        gesamt_grund = tk.Label(master=self, text="{:,.2f}€".format(data['lohn']))

        bezeichner_bsd = tk.Label(master=self, text="Zuschlag kurzfr. Vermittlung")
        anzahl_bsd = tk.Label(master=self, text="{:,.2f}".format(data['bsd_stunden']))
        wert_bsd = tk.Label(master=self, text="{:,.2f}€".format(data['bsd'] * 0.2))
        gesamt_bsd = tk.Label(master=self, text="{:,.2f}€".format(data['bsd_kumuliert']))

        bezeichner_nacht = tk.Label(master=self, text="Nachtzuschläge")
        anzahl_nacht = tk.Label(master=self, text="{:,.2f}".format(data['nachtstunden']))
        wert_nacht = tk.Label(master=self, text="{:,.2f}€".format(data['nachtzuschlag']))
        gesamt_nacht = tk.Label(master=self, text="{:,.2f}€".format(data['nachtzuschlag_kumuliert']))

        bezeichner_kopf.grid(row=0, column=0)
        anzahl_kopf.grid(row=0, column=1)
        wert_kopf.grid(row=0, column=2)
        gesamt_kopf.grid(row=0, column=3)

        bezeichner_grund.grid(row=1, column=0)
        anzahl_grund.grid(row=1, column=1)
        wert_grund.grid(row=1, column=2)
        gesamt_grund.grid(row=1, column=3)

        bezeichner_nacht.grid(row=2, column=0)
        anzahl_nacht.grid(row=2, column=1)
        wert_nacht.grid(row=2, column=2)
        gesamt_nacht.grid(row=2, column=3)

        bezeichner_bsd.grid(row=3, column=0)
        anzahl_bsd.grid(row=3, column=1)
        wert_bsd.grid(row=3, column=2)
        gesamt_bsd.grid(row=3, column=3)


        pass
