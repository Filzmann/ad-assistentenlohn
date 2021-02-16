import tkinter as tk
from datetime import datetime

from Helpers.scollable_frame import VerticalScrolledFrame


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
        self.make_button(button_type="kill",
                         command=data['kill_command'],
                         row=zeilennummer,
                         col=1,
                         parent=parent)
        self.make_button(button_type="edit",
                         command=data['edit_command'],
                         row=zeilennummer,
                         col=2,
                         parent=parent)
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
        self.zelle(parent=parent, inhalt=data['zuschlaege'], row=zeilennummer, col=20, width=23)

        self.zelle(parent=parent, inhalt=data['orgazulage_schicht'], row=zeilennummer, col=21, width=8)
        self.zelle(parent=parent, inhalt=data['wechselzulage_schicht'], row=zeilennummer, col=22, width=8)

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

    def kopfzeile(self, parent):
        # kopfzeile erstellen
        # spalten 0-9 werden für Buttons freigehalten
        # 1. label ist button-spacer
        tk.Label(parent, text='', borderwidth=1, relief="solid", width=8).grid(row=0, column=0)
        tk.Label(parent, text='Tag', borderwidth=1, relief="solid", width=6).grid(row=0, column=10,
                                                                                  columnspan=2)
        tk.Label(parent, text='von', borderwidth=1, relief="solid", width=5).grid(row=0, column=12)
        tk.Label(parent, text='bis', borderwidth=1, relief="solid", width=5).grid(row=0, column=13)
        tk.Label(parent, text='ASN', borderwidth=1, relief="solid", width=8).grid(row=0, column=14)
        tk.Label(parent, text='Std', borderwidth=1, relief="solid", width=5).grid(row=0, column=15)
        tk.Label(parent, text='Grundlohn', borderwidth=1, relief="solid", width=8).grid(row=0, column=16)
        tk.Label(parent, text='kurzfr.', borderwidth=1, relief="solid", width=8).grid(row=0, column=17)
        tk.Label(parent, text='NachtStd', borderwidth=1, relief="solid", width=8).grid(row=0, column=18)
        tk.Label(parent, text='Nachtzu.', borderwidth=1, relief="solid", width=8).grid(row=0, column=19)
        tk.Label(parent, text='Zuschlaege', borderwidth=1, relief="solid", width=23).grid(row=0, column=20)
        tk.Label(parent, text='Wechsel', borderwidth=1, relief="solid", width=8).grid(row=0, column=21)
        tk.Label(parent, text='Orga', borderwidth=1, relief="solid", width=8).grid(row=0, column=22)

    def draw(self, data, anzahl_tage, start):
        for child in self.winfo_children():
            child.destroy()
        zeilennummer = 1
        self.kopfzeile(self)
        scrollframe = VerticalScrolledFrame(self, width=800, height=500)
        scrollframe.grid(row=1, column=0, sticky=tk.NSEW, columnspan=23)
        if data:
            for tag in range(1, anzahl_tage + 1):
                heute = datetime(day=tag, month=start.month, year=start.year)
                # tag als string muss mit führender 0 starten. dafür zfill
                if str(tag).zfill(2) in data.keys():
                    for eintrag in data[str(tag).zfill(2)]:
                        self.zeile(data=eintrag, parent=scrollframe.inner, zeilennummer=zeilennummer, heute=heute)
                        zeilennummer += 1
                else:
                    self.leerzeile(parent=scrollframe.inner, zeilennummer=zeilennummer, heute=heute)
                    zeilennummer += 1

    def make_button(self, button_type, command, parent,
                    row=0,
                    col=0,
                    datum: datetime = None):
        button = image = 0

        if button_type == 'kill':
            image = "images/del.png"
            label = "Löschen"
            button = tk.Button(parent, text=label, command=command)
        elif button_type == 'edit':
            label = "Bearbeiten"
            button = tk.Button(parent,
                               text=label,
                               command=command)
            image = "images/edit.png"
        elif button_type == 'new':
            label = "Neue Schicht"

            button = tk.Button(parent,
                               text=label,
                               command=command)
            image = "images/add.png"

        button.image = tk.PhotoImage(file=image, width=16, height=16)
        button.config(image=button.image, width=16, height=16)
        button.grid(row=row, column=col)
        return button
