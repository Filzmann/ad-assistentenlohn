import datetime
from arbeitszeit import Schicht
import tkinter as tk
from fenster_neuer_as import FensterNeuerAS
from fenster_neue_schicht import FensterNeueSchicht
from menueleiste import Menuleiste


class Hauptfenster(tk.Frame):
    class Begruessung(tk.Frame):
        def __init__(self, parent, assistent):
            super().__init__(parent)
            self.parent = parent
            self.assistent = assistent
            self.info_text = tk.Label(self, text="Bitte erstelle oder öffne eine Assistenten-Datei")
            self.info_text.grid(row=0, column=0, columnspan=2)
            self.button_oeffnen = tk.Button(self,
                                            text="Gespeicherten Assistenten laden",
                                            command=parent.load_and_redraw)
            self.button_oeffnen.grid(row=1, column=0)
            self.button_neu = tk.Button(self, text="Neuen Assistenten anlegen",
                                        command=lambda: FensterNeuerAS(parent.parent, assistent=assistent))
            self.button_neu.grid(row=1, column=1)

        def show(self):
            self.grid()

        def hide(self):
            self.grid_remove()

    class Hauptseite(tk.Frame):
        class Title(tk.Frame):
            def __init__(self, parent, assistent):
                super().__init__(parent)
                hallo = tk.Label(self, text="Hallo " + str(assistent))
                hallo.grid(row=0, column=0)

        class Navigation(tk.Frame):
            def __init__(self, parent, assistent, offset=0):
                super().__init__(parent)
                self.parent = parent
                self.offset = offset
                self.assistent = assistent
                # offset = 0
                vormonat = tk.Button(self, text='einen Monat Zurück', command=lambda: self.monat_change(-1))
                self.arbeitsdate = self.berechne_arbeitsdate()
                self.parent.seitenleiste.arbeitsdatum = self.arbeitsdate
                self.aktueller_monat = tk.Label(self, text=self.arbeitsdate.strftime("%B %Y"))
                naechster_monat = tk.Button(self, text='Nächster Monat', command=lambda: self.monat_change(+1))

                # in den frame packen
                vormonat.grid(row=0, column=0)
                self.aktueller_monat.grid(row=0, column=1)
                naechster_monat.grid(row=0, column=2)

            def berechne_arbeitsdate(self):
                # lieber datum der letzten eingetragenen schicht
                # aktuelles_datum = datetime.date.today()
                dt = self.assistent.letzte_eingetragene_schicht.beginn
                aktuelles_datum = datetime.date(year=dt.year, month=dt.month, day=1)
                jahrmonat = divmod(aktuelles_datum.month + self.offset, 12)
                jahroffset = jahrmonat[0]
                monat = jahrmonat[1]
                if monat == 0:
                    monat = 12
                    jahroffset -= 1
                return datetime.date(aktuelles_datum.year + jahroffset, monat, 1)

            def monat_change(self, step):
                root = self.parent.parent.parent
                self.offset += step
                self.arbeitsdate = self.berechne_arbeitsdate()
                # Hack date in datetime übersetzen
                # TODO  konsequent datetime verwenden.
                self.arbeitsdate = datetime.datetime(self.arbeitsdate.year,
                                                     self.arbeitsdate.month,
                                                     1)
                self.aktueller_monat.config(text=self.arbeitsdate.strftime("%B %Y"))
                root.fenster.hauptseite.tab.destroy()
                root.fenster.hauptseite.seitenleiste.destroy()
                root.fenster.hauptseite.seitenleiste = \
                    root.fenster.hauptseite.Seitenleiste(root.fenster.hauptseite, self.assistent, self.arbeitsdate)
                root.fenster.hauptseite.seitenleiste.arbeitsdatum = self.arbeitsdate
                root.fenster.hauptseite.tab = root.fenster.hauptseite.Tabelle(parent=root.fenster.hauptseite,
                                                                              assistent=self.assistent,
                                                                              arbeitsdatum=self.arbeitsdate)

                root.fenster.hauptseite.tab.grid(row=2, column=0)
                root.fenster.hauptseite.seitenleiste.draw()
                root.fenster.hauptseite.seitenleiste.grid(row=2, column=1)

        class Tabelle(tk.Frame):
            class Zeile:
                def __init__(self, parent, data, assistent, zeilennummer=1):
                    self.parent = parent
                    self.assistent = assistent
                    self.arbeitsdatum = self.parent.arbeitsdatum
                    self.heute = datetime.datetime(self.parent.arbeitsdatum.year,
                                                   self.parent.arbeitsdatum.month, data[0])
                    self.schichtlohn = 0
                    self.stunden = 0
                    if data[1] == 'empty' and not self.assistent.check_au(self.heute) \
                            and not self.assistent.check_urlaub(self.heute):
                        self.leerzeile(zeilennummer=zeilennummer)
                    else:
                        if not self.assistent.check_urlaub(self.heute) \
                                and not self.assistent.check_au(self.heute):
                            self.make_button(command="edit", schicht=data[1], row=zeilennummer, col=0)
                            self.make_button(command="kill", schicht=data[1], row=zeilennummer, col=1)
                            self.make_button(command="new", row=zeilennummer, col=2, datum=self.heute)
                        else:
                            self.make_button(command="kill", datum=self.heute, row=zeilennummer, col=1)
                        # Wochentag
                        tag = self.heute.strftime('%a')
                        self.zelle(inhalt=tag, row=zeilennummer, col=10, width=4)

                        # Tag als Nummer
                        tag = data[0]
                        self.zelle(inhalt=tag, row=zeilennummer, col=11, width=3)
                        if not self.assistent.check_urlaub(self.heute) \
                                and not self.assistent.check_au(self.heute):
                            # Schichtbeginn
                            self.zelle(inhalt=data[1].beginn.strftime('%H:%M'), row=zeilennummer, col=12, width=5)

                            # Schichtende
                            self.zelle(inhalt=data[1].ende.strftime('%H:%M'), row=zeilennummer, col=13, width=5)

                        # ASN/AU/Urlaub/sonstiges
                        inhalt = self.get_inhalt_asn_etc(data)
                        self.zelle(inhalt=inhalt, row=zeilennummer, col=14, width=10)

                        # Stunden
                        inhalt = self.get_inhalt_stunden(data)
                        self.zelle(inhalt=inhalt, row=zeilennummer, col=15, width=5)

                        # Lohn
                        inhalt = self.get_inhalt_lohn(data)
                        self.zelle(inhalt=inhalt, row=zeilennummer, col=16, width=8)

                        if not self.assistent.check_urlaub(self.heute) \
                                and not self.assistent.check_au(self.heute):
                            # BSD/RB
                            inhalt = self.get_inhalt_bsd_rb(data)
                            self.zelle(inhalt=inhalt, row=zeilennummer, col=17, width=8)

                            # Nacht
                            if data[1].nachtstunden > 0:
                                inhalt = "{:,.2f}".format(data[1].nachtstunden)
                                self.parent.parent.seitenleiste.nachtstunden += data[1].nachtstunden
                                self.zelle(inhalt=inhalt, row=zeilennummer, col=18, width=8)

                                nachtzuschlag_schicht = data[1].nachtzuschlag_schicht
                                self.parent.parent.seitenleiste.nachtzuschlag += data[1].nachtzuschlag_schicht
                                self.parent.parent.seitenleiste.nachtzuschlag_pro_stunde = data[1].nachtzuschlag
                                inhalt = "{:,.2f}€".format(nachtzuschlag_schicht)
                                self.zelle(inhalt=inhalt, row=zeilennummer, col=19, width=8)
                                inhalt = ''

                            # Zuschläge Stunden und Grund
                            if data[1] != 'empty' and data[1].zuschlaege != {}:
                                grund = data[1].zuschlaege['zuschlagsgrund']
                                zuschlag_stunden = data[1].zuschlaege['stunden_gesamt']
                                if zuschlag_stunden > 0:
                                    self.parent.parent.seitenleiste.zuschlaege[grund]['stunden_gesamt'] += \
                                        zuschlag_stunden
                                    inhalt = str(zuschlag_stunden) + ' ' + data[1].zuschlaege['zuschlagsgrund']
                                    self.zelle(inhalt=inhalt, row=zeilennummer, col=20, width=15)

                            # Zuschläge Geld
                            if data[1] != 'empty' and data[1].zuschlaege != {}:
                                grund = data[1].zuschlaege['zuschlagsgrund']
                                zuschlag_schicht = data[1].zuschlaege['zuschlag_schicht']
                                if zuschlag_schicht > 0:
                                    self.parent.parent.seitenleiste.zuschlaege[grund]['zuschlaege_gesamt'] \
                                        += zuschlag_schicht
                                    self.parent.parent.seitenleiste.zuschlaege[grund]['zuschlag_pro_stunde'] = \
                                        data[1].zuschlaege['zuschlag_pro_stunde']
                                    inhalt = "{:,.2f}€".format(zuschlag_schicht)
                                    self.zelle(inhalt=inhalt, row=zeilennummer, col=21, width=8)

                            # wechselschichtzulage
                            if data[1] != 'empty':
                                self.parent.parent.seitenleiste.wechselschichtzulage += data[
                                    1].wechselschichtzulage_schicht
                                self.parent.parent.seitenleiste.wechselschichtzulage_pro_stunde = data[
                                    1].wechselschichtzulage
                                inhalt = "{:,.2f}€".format(data[1].wechselschichtzulage_schicht)
                            self.zelle(inhalt=inhalt, row=zeilennummer, col=22, width=8)

                            if data[1] != 'empty':
                                self.parent.parent.seitenleiste.orga += data[1].orgazulage_schicht
                                self.parent.parent.seitenleiste.orga_pro_stunde = data[1].orgazulage
                                inhalt = "{:,.2f}€".format(data[1].orgazulage_schicht)
                            self.zelle(inhalt=inhalt, row=zeilennummer, col=23, width=8)

                def leerzeile(self, zeilennummer):
                    self.make_button(command="new", row=zeilennummer, col=2, datum=self.heute)
                    tag = self.heute.strftime('%a')
                    self.zelle(inhalt=tag, row=zeilennummer, col=10, width=4)
                    # Tag als Nummer
                    tag = self.heute.strftime('%d')
                    self.zelle(inhalt=tag, row=zeilennummer, col=11, width=3)

                def make_button(self, command,
                                schicht: Schicht = None,
                                row=0,
                                col=0,
                                datum: datetime.datetime = None):
                    button = image = 0
                    if schicht:
                        if schicht.original_schicht != "root":
                            key_string = schicht.original_schicht
                            schicht = self.assistent.schichten[schicht.original_schicht]
                        else:
                            key_string = schicht.beginn.strftime('%Y%m%d%H%M')

                    if command == 'kill':
                        image = "images/del.png"
                        label = "Löschen"
                        if schicht:
                            button = tk.Button(self.parent, text=label, command=lambda: self.kill_schicht(key_string))
                        else:
                            button = tk.Button(self.parent, text=label, command=lambda: self.kill_au_urlaub(datum))
                    elif command == 'edit':
                        label = "Bearbeiten"
                        button = tk.Button(self.parent,
                                           text=label,
                                           command=lambda: FensterNeueSchicht(parent=self.parent.parent,
                                                                              assistent=self.assistent,
                                                                              edit_schicht=schicht))
                        image = "images/edit.png"
                    elif command == 'new':
                        label = "Neue Schicht"

                        button = tk.Button(self.parent,
                                           text=label,
                                           command=lambda: FensterNeueSchicht(parent=self.parent.parent,
                                                                              assistent=self.assistent,
                                                                              datum=datum))
                        image = "images/add.png"

                    button.image = tk.PhotoImage(file=image, width=16, height=16)
                    button.config(image=button.image, width=16, height=16)
                    button.grid(row=row, column=col)
                    return button

                def kill_schicht(self, key):
                    schicht = self.assistent.schichten[key]
                    self.assistent.letzte_eingetragene_schicht = schicht
                    self.assistent.delete_schicht(key=key)
                    self.assistent.save_to_file()
                    self.parent.parent.parent.redraw(assistent=self.assistent)

                def kill_au_urlaub(self, datum):
                    if not self.assistent.delete_urlaub(datum):
                        self.assistent.delete_au(datum)
                    self.assistent.save_to_file()
                    self.parent.parent.parent.redraw(assistent=self.assistent)

                def zelle(self, inhalt='', width=5, row=0, col=0):
                    if inhalt:
                        zelle = tk.Entry(self.parent, width=width)
                        zelle.grid(row=row, column=col)
                        zelle.delete(0, "end")
                        zelle.insert(0, inhalt)
                        zelle.config(state='readonly')
                        return zelle

                def get_inhalt_asn_etc(self, data):
                    inhalt = ''
                    if self.parent.assistent.check_au(datetime.datetime(self.arbeitsdatum.year,
                                                                        self.arbeitsdatum.month, data[0], 0, 1)):
                        inhalt = 'AU'
                    elif self.parent.assistent.check_urlaub(datetime.datetime(self.arbeitsdatum.year,
                                                                              self.arbeitsdatum.month, data[0], 0, 1)):
                        inhalt = 'Urlaub'
                    elif data[1] != 'empty':
                        inhalt = ''
                        # TODO andere Lohnarten für Ausfallgeld, Berechnung Wegegeld
                        if data[1].ist_ausfallgeld:
                            inhalt += "Ausf."
                        if data[1].ist_assistententreffen:
                            inhalt += "AT "
                        if data[1].ist_pcg:
                            inhalt += "PCG "
                        inhalt += data[1].asn.kuerzel
                    return inhalt

                def get_inhalt_stunden(self, data):
                    assistent = self.parent.assistent
                    if assistent.check_au(datetime.datetime(self.arbeitsdatum.year,
                                                            self.arbeitsdatum.month, data[0], 0, 1)):
                        # krank
                        au = assistent.check_au(datetime.datetime(self.arbeitsdatum.year, self.arbeitsdatum.month,
                                                                  data[0], 0, 1))
                        au.calculate()
                        austunden = au.berechne_durchschnittliche_stundenzahl_pro_tag()['stunden']
                        self.stunden = austunden
                        self.parent.parent.seitenleiste.austunden += austunden
                    elif assistent.check_urlaub(datetime.datetime(self.arbeitsdatum.year,
                                                                  self.arbeitsdatum.month, data[0], 0, 1)):
                        # Urlaub
                        urlaub = assistent.check_urlaub(
                            datetime.datetime(self.arbeitsdatum.year, self.arbeitsdatum.month,
                                              data[0], 0, 1))
                        urlaub.calculate()
                        ustunden = urlaub.berechne_durchschnittliche_stundenzahl_pro_tag()['stunden']
                        self.stunden = ustunden
                        self.parent.parent.seitenleiste.ustunden += ustunden
                    elif data[1] != 'empty':
                        self.parent.parent.seitenleiste.arbeitsstunden += data[1].stundenzahl
                        self.stunden = data[1].berechne_stundenzahl()
                    if self.stunden > 0:
                        inhalt = "{:,.2f}".format(self.stunden)
                        return inhalt

                def get_inhalt_lohn(self, data):
                    inhalt = ''
                    assistent = self.parent.assistent
                    heute = datetime.datetime(self.arbeitsdatum.year, self.arbeitsdatum.month, data[0], 0, 1)
                    if assistent.check_au(heute):
                        au = assistent.check_au(heute)
                        au.calculate()
                        aulohn = au.aulohn_pro_tag
                        aulohn_pro_stunde = au.aulohn_pro_stunde
                        self.parent.parent.seitenleiste.aulohn += aulohn
                        self.parent.parent.seitenleiste.aulohn_pro_stunde = aulohn_pro_stunde
                        if aulohn > 0:
                            inhalt = "{:,.2f}€".format(aulohn)
                    elif assistent.check_urlaub(heute):
                        urlaub = assistent.check_urlaub(heute)
                        urlaub.calculate()
                        ulohn = urlaub.ulohn_pro_tag
                        ulohn_pro_stunde = urlaub.ulohn_pro_stunde
                        self.parent.parent.seitenleiste.ulohn += ulohn
                        self.parent.parent.seitenleiste.ulohn_pro_stunde = ulohn_pro_stunde
                        if ulohn > 0:
                            inhalt = "{:,.2f}€".format(ulohn)
                    elif data[1] != 'empty':
                        schichtlohn = data[1].schichtlohn
                        self.parent.parent.seitenleiste.grundlohn += data[1].schichtlohn
                        self.parent.parent.seitenleiste.grundlohn_pro_stunde = data[1].stundenlohn
                        if schichtlohn > 0:
                            inhalt = "{:,.2f}€".format(schichtlohn)
                    return inhalt

                def get_inhalt_bsd_rb(self, data):
                    if data[1].ist_kurzfristig:
                        kurzfr = data[1].schichtlohn * 0.2
                        self.parent.parent.seitenleiste.kurzfr_pro_stunde = data[1].stundenlohn * 0.2
                        self.parent.parent.seitenleiste.kurzfr_stunden = data[1].stundenzahl
                        self.parent.parent.seitenleiste.kurzfr += kurzfr
                        return "{:,.2f}€".format(kurzfr)

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

            """baut die Tabelle auf der Hauptseite auf. """

            def __init__(self,
                         parent,
                         assistent,
                         arbeitsdatum=datetime.datetime(datetime.date.today().year,
                                                        datetime.date.today().month,
                                                        1)):
                super().__init__(parent, bd=1)
                self.parent = parent
                self.assistent = assistent
                self.start = self.arbeitsdatum = arbeitsdatum
                self.end = self.verschiebe_monate(1, arbeitsdatum)
                self.schichten = self.assistent.get_all_schichten(self.start, self.end)
                # wenn noch keine Schichten eingetragen wurden, die Tabelle also leer bleibt, wird gecheckt,
                # ob es regelmäßige Schichten gibt, welche eingetragen und dem AS hinzugefügt werden.
                if not self.schichten:
                    self.schichten = self.insert_standardschichten(self.start, self.end)
                schichten_sortiert = self.split_schichten_um_mitternacht()
                schichten_sortiert = self.sort_und_berechne_schichten_by_day(schichten_sortiert, arbeitsdatum)

                # Tabelle aufbauen
                self.kopfzeile()

                # körper

                zaehler = 0
                for zeilendaten in schichten_sortiert:
                    zaehler += 1
                    self.Zeile(self, zeilendaten, assistent=self.assistent,
                               zeilennummer=zaehler)

            def split_schichten_um_mitternacht(self):
                ausgabe = []
                for schicht in self.schichten.values():
                    if not schicht.teilschichten:
                        ausgabe.append(schicht)
                    else:
                        for teilschicht in schicht.teilschichten:
                            ausgabe.append(teilschicht)
                return ausgabe

            @staticmethod
            def verschiebe_monate(offset, datum=datetime.datetime.now()):
                arbeitsmonat = datum.month + offset
                tmp = divmod(arbeitsmonat, 12)
                offset_arbeitsjahr = tmp[0]
                arbeitsmonat = tmp[1]
                if arbeitsmonat == 0:
                    arbeitsmonat = 12
                    offset_arbeitsjahr -= 1
                if offset_arbeitsjahr < 0:
                    # modulo einer negativen Zahl ist ein Arschloch..hoffentlich stimmts
                    # TODO eventuell jahr korrigieren? Testen, was passiert
                    arbeitsmonat = 12 - arbeitsmonat
                arbeitsjahr = datum.year + offset_arbeitsjahr
                arbeitsdatum = datetime.datetime(arbeitsjahr, arbeitsmonat, 1, 0, 0, 0)
                return arbeitsdatum

            def insert_standardschichten(self, erster_tag, letzter_tag):
                def get_ersten_xxtag(int_weekday, erster=datetime.datetime.now()):
                    for counter in range(1, 8):
                        if datetime.datetime(year=erster.year, month=erster.month, day=counter, hour=0,
                                             minute=0).weekday() == int_weekday:
                            return counter

                assistent = self.assistent
                feste_schichten = assistent.festeSchichten
                wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
                for schicht in feste_schichten:
                    wtag_int = wochentage.index(schicht["wochentag"])
                    erster_xxtag_des_monats = get_ersten_xxtag(wtag_int, erster_tag)
                    monat = erster_tag.month
                    year = erster_tag.year
                    maxday = letzter_tag - datetime.timedelta(days=1)
                    maxday = int(maxday.strftime("%d"))
                    kuerzel = schicht["asn"]
                    asn = assistent.get_asn_by_kuerzel(kuerzel)
                    for woche in range(0, 4):
                        tag = woche * 7 + erster_xxtag_des_monats
                        if tag <= maxday:
                            if schicht["start"] < schicht["ende"]:
                                start = datetime.datetime(year=year,
                                                          month=monat,
                                                          day=tag,
                                                          hour=schicht["start"].hour,
                                                          minute=schicht["start"].minute)
                                end = datetime.datetime(year=year,
                                                        month=monat,
                                                        day=tag,
                                                        hour=schicht["ende"].hour,
                                                        minute=schicht["ende"].minute)
                            # nachtschicht. es gibt keine regelmäßigen dienstreisen!
                            else:
                                start = datetime.datetime(year=year,
                                                          month=monat,
                                                          day=tag,
                                                          hour=schicht["start"].hour,
                                                          minute=schicht["start"].minute)
                                end = datetime.datetime(year=year,
                                                        month=monat,
                                                        day=tag,
                                                        hour=schicht["ende"].hour,
                                                        minute=schicht["ende"].minute) + datetime.timedelta(days=1)
                            if not assistent.check_au(start) and not assistent.check_urlaub(start) \
                                    and not assistent.check_au(end - datetime.timedelta(minutes=1)) \
                                    and not assistent.check_urlaub(end - datetime.timedelta(minutes=1)):
                                schicht_neu = Schicht(beginn=start, ende=end, asn=asn, assistent=assistent)
                                assistent.schicht_dazu(schicht_neu)

                return assistent.get_all_schichten(erster_tag, letzter_tag)

            @staticmethod
            def sort_und_berechne_schichten_by_day(schichten, monatjahr=datetime.date.today()):
                def end_of_month(month, year):
                    if month == 12:
                        month = 1
                        year += 1
                    else:
                        month += 1
                    return datetime.date(year, month, 1) - datetime.timedelta(days=1)

                """bekommt eine Liste von Schichten, und schickt eine Liste von Paaren von Tag, Schicht zurück """
                monat = int(monatjahr.strftime('%m'))
                jahr = int(monatjahr.strftime('%Y'))
                anzahl_tage = int(end_of_month(monat, jahr).strftime('%d'))
                ausgabe = []

                for tag in range(1, anzahl_tage + 1):
                    tag_isset = 0
                    # TODO Monatsgrenzen anschauen
                    for schicht in schichten:
                        if tag == int(schicht.beginn.strftime('%d')):
                            paar = [tag, schicht]
                            ausgabe.append(paar)
                            tag_isset = 1
                    if tag_isset == 0:
                        ausgabe.append([tag, 'empty'])

                return ausgabe

        class Seitenleiste(tk.Frame):
            class Zeile(tk.Frame):
                def __init__(self, parent, spalte1, spalte4, spalte2='', spalte3=''):
                    super().__init__(parent)
                    a = tk.Label(self, text=spalte1, justify="left")
                    b = tk.Label(self, text=spalte2, justify="right")
                    c = tk.Label(self, text=spalte3, justify="right")
                    d = tk.Label(self, text=spalte4, justify="right")

                    a.config(width=15)
                    b.config(width=10)
                    c.config(width=10)
                    d.config(width=10)

                    a.grid(row=0, column=0, sticky="w")
                    b.grid(row=0, column=1, sticky="e")
                    c.grid(row=0, column=2, sticky="e")
                    d.grid(row=0, column=3, sticky="e")

            def __init__(self, parent, assistent=None, arbeitsdatum=None):
                super().__init__(parent)
                self.assistent = assistent
                self.parent = parent
                self.arbeitsdatum = arbeitsdatum
                self.zuschlaege = {}
                for zuschlag_name in parent.assistent.lohntabelle.zuschlaege.keys():
                    self.zuschlaege[zuschlag_name] = {
                        'stunden_gesamt': 0,
                        'zuschlaege_gesamt': 0,
                        'stunden_steuerfrei': 0,
                        'stunden_steuerpflichtig': 0,
                        'zuschlag_pro_stunde': 0,
                    }
                self.arbeitsstunden = 0
                self.grundlohn = 0
                self.grundlohn_pro_stunde = 0
                self.ustunden = 0
                self.ulohn = 0
                self.ulohn_pro_stunde = 0
                self.austunden = 0
                self.aulohn = 0
                self.aulohn_pro_stunde = 0
                self.kurzfr = 0
                self.kurzfr_pro_stunde = 0
                self.kurzfr_stunden = 0
                self.nachtstunden = 0
                self.nachtzuschlag = 0
                self.nachtzuschlag_pro_stunde = 0
                self.wechselschichtzulage = 0
                self.wechselschichtzulage_pro_stunde = 0
                self.orga = 0
                self.orga_pro_stunde = 0
                self.anzahl_feiertage = self.zaehle_feiertage(self.arbeitsdatum)
                self.freizeitausgleich = self.berechne_freizeitausgleich(self.anzahl_feiertage)

            def draw(self):
                zeilenzaehler = 0
                zeile = self.Zeile(self,
                                   spalte1='Bezeichnung',
                                   spalte2="Stunden",
                                   spalte3="pro Stunde",
                                   spalte4="gesamt")
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                zeile = self.Zeile(self,
                                   spalte1='Grundlohn',
                                   spalte2="{:,.2f}".format(self.arbeitsstunden),
                                   spalte3="{:,.2f}€".format(self.grundlohn_pro_stunde),
                                   spalte4="{:,.2f}€".format(self.grundlohn))
                zeile.grid(row=zeilenzaehler, column=0)
                if self.ulohn:
                    zeilenzaehler += 1
                    zeile = self.Zeile(self,
                                       spalte1='Entgelt Urlaub',
                                       spalte2="{:,.2f}".format(self.ustunden),
                                       spalte3="{:,.2f}€".format(self.ulohn_pro_stunde),
                                       spalte4="{:,.2f}€".format(self.ulohn))
                    zeile.grid(row=zeilenzaehler, column=0)
                if self.aulohn:
                    zeilenzaehler += 1
                    zeile = self.Zeile(self,
                                       spalte1='Entgelt Arbeitsunfähigkeit',
                                       spalte2="{:,.2f}".format(self.austunden),
                                       spalte3="{:,.2f}€".format(self.aulohn_pro_stunde),
                                       spalte4="{:,.2f}€".format(self.aulohn))
                    zeile.grid(row=zeilenzaehler, column=0)
                if self.kurzfr:
                    zeilenzaehler += 1
                    zeile = self.Zeile(self,
                                       spalte1='Kurzfr. RB',
                                       spalte2="{:,.2f}".format(self.kurzfr_stunden),
                                       spalte3="{:,.2f}€".format(self.kurzfr_pro_stunde),
                                       spalte4="{:,.2f}€".format(self.kurzfr))
                    zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                zeile = self.Zeile(self,
                                   spalte1='Nacht',
                                   spalte2="{:,.2f}".format(self.nachtstunden),
                                   spalte3="{:,.2f}€".format(self.nachtzuschlag_pro_stunde),
                                   spalte4="{:,.2f}€".format(self.nachtstunden))
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                zeile = self.Zeile(self,
                                   spalte1='Wechselschicht',
                                   spalte2="{:,.2f}".format(self.arbeitsstunden),
                                   spalte3="{:,.2f}€".format(self.wechselschichtzulage_pro_stunde),
                                   spalte4="{:,.2f}€".format(self.wechselschichtzulage))
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                zeile = self.Zeile(self,
                                   spalte1='Orga',
                                   spalte2="{:,.2f}".format(self.arbeitsstunden),
                                   spalte3="{:,.2f}€".format(self.orga_pro_stunde),
                                   spalte4="{:,.2f}€".format(self.orga))
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                brutto = self.grundlohn + self.aulohn + self.ulohn + self.wechselschichtzulage + \
                         self.nachtzuschlag + self.orga + self.kurzfr
                for zuschlag in self.zuschlaege:
                    if self.zuschlaege[zuschlag]["stunden_gesamt"] > 0:
                        zeile = self.Zeile(self,
                                           spalte1=zuschlag,
                                           spalte2="{:,.2f}".format(self.zuschlaege[zuschlag]["stunden_gesamt"]),
                                           spalte3="{:,.2f}€".format(self.zuschlaege[zuschlag]["zuschlag_pro_stunde"]),
                                           spalte4="{:,.2f}€".format(self.zuschlaege[zuschlag]["zuschlaege_gesamt"]))
                        zeile.grid(row=zeilenzaehler, column=0)
                        brutto += self.zuschlaege[zuschlag]["zuschlaege_gesamt"]
                        zeilenzaehler += 1

                zeile = self.Zeile(self,
                                   spalte1='Nicht gewährter Freizeitausgleich',
                                   spalte4="{:,.2f}€".format(self.freizeitausgleich))
                zeile.grid(row=zeilenzaehler, column=0)
                brutto += self.freizeitausgleich
                zeilenzaehler += 1
                zeile = self.Zeile(self,
                                   spalte1='Bruttolohn',
                                   spalte4="{:,.2f}€".format(brutto))
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1
                bruttokey = self.arbeitsdatum.strftime("%Y-%m")
                self.assistent.bruttoloehne[bruttokey] = {'stunden': self.arbeitsstunden, 'geld': brutto}

            def zaehle_feiertage(self, datum: datetime.datetime = None):

                startdatum = datum
                feiertage = 0
                while datum.month == startdatum.month:
                    if self.check_feiertag(datum=datum):
                        if not self.assistent.check_au(datum) and not self.assistent.check_urlaub(datum):
                            feiertage += 1
                    datum += datetime.timedelta(days=1)
                return feiertage

            def berechne_freizeitausgleich(self, anzahl_feiertage=0):
                return anzahl_feiertage * self.berechne_tagessatz()

            def berechne_tagessatz(self):
                keys = []
                date = datetime.date(self.arbeitsdatum.year, self.arbeitsdatum.month, 1)
                for zaehler in range(1, 7):
                    letzter_des_vormonats = date - datetime.timedelta(days=1)
                    anzahl_tage_vormonat = int(letzter_des_vormonats.strftime('%d'))
                    date = letzter_des_vormonats - datetime.timedelta(days=anzahl_tage_vormonat - 1)
                    key = date.strftime('%Y-%m')
                    keys.append(key)
                summe_brutto = 0
                summe_stunden = 0
                anzahl_monate = 0
                for key in keys:
                    if key in self.assistent.bruttoloehne:
                        summe_brutto += self.assistent.bruttoloehne[key]['geld']
                        summe_stunden += self.assistent.bruttoloehne[key]['stunden']
                        anzahl_monate += 1

                schnitt_stundenlohn = summe_brutto / summe_stunden
                # wir rechnen mit durchschnittlich 30 Tage pro Monat
                schnitt_stunden_pro_tag = summe_stunden / (30 * anzahl_monate)

                return schnitt_stunden_pro_tag * schnitt_stundenlohn

            def check_feiertag(self, datum):
                # TODO in einer funktion mit gleichnamiger methode in Schicht zusammenführen
                jahr = datum.year
                feiertage = []
                feiertag = {'name': 'Neujahr', 'd': 1, 'm': 1, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': 'Internationaler Frauentag', 'd': 8, 'm': 3, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': 'Tag der Arbeit', 'd': 1, 'm': 5, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': 'Tag der deutschen Einheit', 'd': 3, 'm': 10, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': '1. Weihnachtsfeiertagt', 'd': 25, 'm': 12, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': '2. Weihnachtsfeiertag', 'd': 26, 'm': 12, 'Y': 0}
                feiertage.append(feiertag)
                feiertag = {'name': 'Tag der Befreiung', 'd': 26, 'm': 12, 'Y': 2020}
                feiertage.append(feiertag)

                # kein Feiertag in Berlin TODO Prio = 1000, andere Bundesländer
                ostersonntag = self.berechne_ostern(jahr)
                karfreitag = ostersonntag - datetime.timedelta(days=2)
                feiertag = {'name': 'Karfreitag', 'd': int(karfreitag.strftime('%d')),
                            'm': int(karfreitag.strftime('%m')), 'Y': 0}
                feiertage.append(feiertag)
                ostermontag = ostersonntag + datetime.timedelta(days=1)
                feiertag = {'name': 'Ostermontag', 'd': int(ostermontag.strftime('%d')),
                            'm': int(ostermontag.strftime('%m')), 'Y': 0}
                feiertage.append(feiertag)
                himmelfahrt = ostersonntag + datetime.timedelta(days=40)
                feiertag = {'name': 'Christi Himmelfahrt', 'd': int(himmelfahrt.strftime('%d')),
                            'm': int(himmelfahrt.strftime('%m')), 'Y': 0}
                feiertage.append(feiertag)
                pfingstsonntag = ostersonntag + datetime.timedelta(days=49)
                feiertag = {'name': 'Pfingstsonntag', 'd': int(pfingstsonntag.strftime('%d')),
                            'm': int(pfingstsonntag.strftime('%m')), 'Y': 0}
                feiertage.append(feiertag)
                pfingstmontag = ostersonntag + datetime.timedelta(days=50)
                feiertag = {'name': 'Pfingstmontag', 'd': int(pfingstmontag.strftime('%d')),
                            'm': int(pfingstmontag.strftime('%m')), 'Y': 0}
                feiertage.append(feiertag)
                ausgabe = ''
                for feiertag in feiertage:
                    if feiertag['Y'] > 0:
                        if feiertag['Y'] == datum.year \
                                and datum.day == feiertag['d'] \
                                and datum.month == feiertag['m']:
                            ausgabe = feiertag['name']
                            break
                    elif feiertag['Y'] == 0:
                        if datum.day == feiertag['d'] and datum.month == feiertag['m']:
                            ausgabe = feiertag['name']
                            break
                return ausgabe

            @staticmethod
            def berechne_ostern(jahr):

                # Berechnung von Ostern mittels Gaußscher Osterformel
                # siehe http://www.ptb.de/de/org/4/44/441/oste.htm
                # mindestens bis 2031 richtig
                K = jahr // 100
                M = 15 + ((3 * K + 3) // 4) - ((8 * K + 13) // 25)
                S = 2 - ((3 * K + 3) // 4)
                A = jahr % 19
                D = (19 * A + M) % 30
                R = (D + (A // 11)) // 29
                OG = 21 + D - R
                SZ = 7 - (jahr + (jahr // 4) + S) % 7
                OE = 7 - ((OG - SZ) % 7)

                tmp = OG + OE  # das Osterdatum als Tages des März, also 32 entspricht 1. April
                m = 0
                if tmp > 31:  # Monat erhöhen, tmp=tag erniedriegen
                    m = tmp // 31
                    if tmp == 31:
                        m = 0
                    tmp = tmp - 31

                return datetime.date(jahr, 3 + m, tmp)

        def __init__(self, parent, assistent):  # von Hauptseite
            super().__init__(parent)
            self.assistent = assistent
            self.parent = parent
            dt = self.assistent.letzte_eingetragene_schicht.beginn
            arbeitsdatum = datetime.datetime(dt.year, dt.month, 1)
            self.title = self.Title(self, assistent=assistent)
            self.seitenleiste = self.Seitenleiste(self, assistent=assistent, arbeitsdatum=arbeitsdatum)
            self.nav = self.Navigation(self, assistent=assistent)

            self.tab = self.Tabelle(self, arbeitsdatum=arbeitsdatum, assistent=self.assistent)

            self.title.grid(row=0, column=0, columnspan=2)
            self.nav.grid(row=1, column=0, columnspan=2)
            self.tab.grid(row=2, column=0)
            self.seitenleiste.grid(row=2, column=1)
            self.seitenleiste.draw()

        def show(self):
            self.grid()

        def hide(self):
            self.grid_remove()

    def __init__(self, parent, assistent):  # von Hauptfenster
        super().__init__(parent)
        self.parent = parent
        self.assistent = assistent
        if not self.assistent.assistent_is_loaded:
            self.hello = self.Begruessung(self, self.assistent)
            self.hello.grid(row=0, column=0)
        else:
            self.hauptseite = self.Hauptseite(parent=self, assistent=self.assistent)
            self.hauptseite.grid(row=0, column=0)

    def load_and_redraw(self):
        assistent = self.assistent.load_from_file()
        self.assistent = assistent
        self.parent.assistent = assistent  # der gesamten app bescheid sagen, dass es einen neuen AS gibt

        self.redraw(self.assistent)

    def redraw(self, assistent):
        # menueleiste laden
        self.assistent = assistent
        menuleiste = Menuleiste(self.parent)
        self.parent.config(menu=menuleiste)

        self.parent.fenster.destroy()
        self.parent.fenster = Hauptfenster(self.parent, self.assistent)
        self.parent.fenster.grid(row=0, column=0)
