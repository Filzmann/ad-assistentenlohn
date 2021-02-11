import tkinter as tk
from datetime import datetime


class TabelleView(tk.Frame):
    def __init__(self, parent_view, data, anzahl_tage=31, start=datetime.now()):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        self.draw(data, anzahl_tage, start)


    def zeile(self, data, parent, zeilennummer, heute):
        # self.make_button(command="new", row=zeilennummer, col=2, datum=self.heute)
        tag = heute.strftime('%a')
        self.zelle(parent=parent, inhalt=tag, row=zeilennummer, col=10, width=4, justify='left')
        # Tag als Nummer
        tag = heute.strftime('%d')
        self.zelle(parent=parent, inhalt=tag, row=zeilennummer, col=11, width=3)
        self.zelle(parent=parent, inhalt=data['von'], row=zeilennummer, col=12, width=5)
        self.zelle(parent=parent, inhalt=data['bis'], row=zeilennummer, col=13, width=5)
        self.zelle(parent=parent, inhalt=data['asn'], row=zeilennummer, col=14, width=10)
        self.zelle(parent=parent, inhalt=data['stunden'], row=zeilennummer, col=15, width=5)
        self.zelle(parent=parent, inhalt=data['schichtlohn'], row=zeilennummer, col=16, width=8)
        self.zelle(parent=parent, inhalt=data['bsd'], row=zeilennummer, col=17, width=8)
        self.zelle(parent=parent, inhalt=data['nachtstunden'], row=zeilennummer, col=18, width=8)
        self.zelle(parent=parent, inhalt=data['nachtzuschlag_schicht'], row=zeilennummer, col=19, width=8)
        # 20 so, sa Feiertag, hl Abend, silv
        self.zelle(parent=parent, inhalt=data['zuschlaege'], row=zeilennummer, col=22, width=3)

        self.zelle(parent=parent, inhalt=data['orgazulage_schicht'], row=zeilennummer, col=22, width=3)
        self.zelle(parent=parent, inhalt=data['wechselzulage_schicht'], row=zeilennummer, col=23, width=3)

        # 'zuschlaege': []

    @staticmethod
    def zelle(parent, inhalt='', width=5, row=0, col=0, justify="right"):
        if inhalt:
            zellen_label = tk.Label(parent, width=width, justify=justify, text=inhalt)

            zellen_label.grid(row=row, column=col, sticky="e")
            return zellen_label

    def leerzeile(self, parent, zeilennummer, heute):
        # self.make_button(command="new", row=zeilennummer, col=2, datum=self.heute)
        tag = heute.strftime('%a')
        self.zelle(parent=parent, inhalt=tag, row=zeilennummer, col=10, width=4)
        # Tag als Nummer
        tag = heute.strftime('%d')
        self.zelle(parent=parent, inhalt=tag, row=zeilennummer, col=11, width=3)

    def kopfzeile(self):
        # kopfzeile erstellen
        # spalten 0-9 werden für Buttons freigehalten
        tk.Label(self, text='Tag', borderwidth=1, relief="solid", width=6).grid(row=0, column=10,
                                                                                columnspan=2)
        tk.Label(self, text='von', borderwidth=1, relief="solid", width=5).grid(row=0, column=12)
        tk.Label(self, text='bis', borderwidth=1, relief="solid", width=5).grid(row=0, column=13)
        tk.Label(self, text='ASN', borderwidth=1, relief="solid", width=8).grid(row=0, column=14)
        tk.Label(self, text='Std', borderwidth=1, relief="solid", width=5).grid(row=0, column=15)
        tk.Label(self, text='Grundlohn', borderwidth=1, relief="solid", width=8).grid(row=0, column=16)
        tk.Label(self, text='kurzfr.', borderwidth=1, relief="solid", width=8).grid(row=0, column=17)
        tk.Label(self, text='NachtStd', borderwidth=1, relief="solid", width=8).grid(row=0, column=18)
        tk.Label(self, text='Nachtzu.', borderwidth=1, relief="solid", width=8).grid(row=0, column=19)
        tk.Label(self, text='Zuschlaege', borderwidth=1, relief="solid", width=18).grid(row=0, column=20,
                                                                                        columnspan=2)
        tk.Label(self, text='Wechsel', borderwidth=1, relief="solid", width=8).grid(row=0, column=22)
        tk.Label(self, text='Orga', borderwidth=1, relief="solid", width=8).grid(row=0, column=23)

    def draw(self, data, anzahl_tage, start):
        for child in self.winfo_children():
            child.destroy()
        zeilennummer = 1
        self.kopfzeile()
        if data:
            for tag in range(1, anzahl_tage + 1):
                heute = datetime(day=tag, month=start.month, year=start.year)
                if str(tag) in data.keys():
                    for eintrag in data[str(tag)]:
                        self.zeile(data=eintrag, parent=self, zeilennummer=zeilennummer, heute=heute)
                        zeilennummer += 1
                else:
                    self.leerzeile(parent=self, zeilennummer=zeilennummer, heute=heute)
                    zeilennummer += 1

