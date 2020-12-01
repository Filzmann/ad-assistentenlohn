import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pickle
import datetime
from tkcalendar import Calendar


class TimePicker(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.reg = self.register(self.hour_valid)
        self.hourstr = tk.StringVar(self, '10')
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, validate='focusout', validatecommand=(self.reg, '%P'),
                               invalidcommand=self.hour_invalid, textvariable=self.hourstr, width=2)
        self.reg2 = self.register(self.min_valid)
        self.minstr = tk.StringVar(self, '30')
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, validate='focusout', validatecommand=(self.reg2, '%P'),
                              invalidcommand=self.min_invalid, textvariable=self.minstr, width=2)
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def hour_invalid(self):
        self.hourstr.set('10')

    def hour_valid(self, eingabe):
        if eingabe.isdigit() and int(eingabe) in range(24) and len(eingabe) in range(1, 3):
            valid = True
        else:
            valid = False
        if not valid:
            self.hour.after_idle(lambda: self.hour.config(validate='focusout'))
        return valid

    def min_invalid(self):
        self.minstr.set('30')

    def min_valid(self, eingabe):
        if eingabe.isdigit() and int(eingabe) in range(60) and len(eingabe) in range(1, 3):
            valid = True
        else:
            valid = False
        if not valid:
            self.min.after_idle(lambda: self.min.config(validate='focusout'))
        return valid


class Person:
    name = ""
    vorname = ""
    email = ""
    strasse = ""
    hausnummer = ""
    plz = ""
    stadt = "Berlin"

    def set_adresse(self, strasse, hausnummer, plz, stadt="Berlin"):
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.plz = plz
        self.stadt = stadt


# erstellt den einen AS, kommt genau einmal pro Datei vor
class AS(Person):
    count = 0
    assistent_is_loaded = 0

    def __init__(self, name='', vorname='', email="keine@email.de",
                 einstellungsdatum=datetime.datetime(1970, 1, 1, 0, 0, 0)):
        self.filepath = ''
        self.schichten = {}
        self.asn = {}
        self.name = name
        self.vorname = vorname
        self.email = email
        self.einstellungsdatum = einstellungsdatum
        self.__class__.count += 1
        self.festeSchichten = {}
        self.urlaub = []
        self.au = []

    def __del__(self):
        self.__class__.count -= 1

    def __str__(self):
        return self.vorname + " " + self.name

    def get_all_asn(self):
        return self.asn

    def set_all_asn(self, asn):
        self.asn = asn

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def get_asn_by_kuerzel(self, kuerzel):
        return self.asn[kuerzel]

    def get_all_schichten(self, start=0, end=0):
        """ wenn keine datetimes für start und end angegeben sind, werden alle Schichten ausgegeben,
         ansonsten alle schichten, die größer als start und <= end sind """
        ausgabe = {}
        if start == 0 and end == 0:
            ausgabe = self.schichten
        else:
            for schicht in self.schichten.values():
                beginn_akt_schicht = schicht.beginn
                end_akt_schicht = schicht.ende
                if start <= beginn_akt_schicht < end or start <= end_akt_schicht < end:
                    ausgabe[beginn_akt_schicht.strftime("%Y%m%d%H%M")] = schicht
        return ausgabe

    def delete_schicht(self, schicht='', key=''):
        if key != '' or schicht != '':
            if key == '':
                key = schicht.beginn.strftime('%Y%m%d%H%M')
            del self.schichten[key]

    def set_all_schichten(self, schichten):
        """ Nimmt ein dict von Schichten entgegen und weist diese dem AS zu"""
        self.schichten = schichten

    def asn_dazu(self, asn):
        self.asn[asn.kuerzel] = asn

    def schicht_dazu(self, schicht):
        key = schicht.beginn.strftime("%Y%m%d%H%M")
        self.schichten[key] = schicht

    def urlaub_dazu(self, urlaub):
        self.urlaub.append(urlaub)

    def get_urlaub(self, pruefzeitraum_beginn=0, pruefzeitraum_ende=0):
        # TODO beschränke Zeitraum
        return self.urlaub

    def check_urlaub(self, datum):
        for urlaub in self.urlaub:
            if urlaub.beginn <= datum <= urlaub.ende:
                return urlaub

    def au_dazu(self, au):
        self.au.append(au)

    def check_au(self, datum):
        for au in self.au:
            if au.beginn <= datum <= au.ende:
                return au


# ein AS kann bei mehreren ASN arbeiten
class ASN(Person):
    kuerzel = ''

    def __init__(self, name, vorname, kuerzel, strasse='', hausnummer='', plz='', stadt='Berlin'):
        self.name = name
        self.vorname = vorname
        self.kuerzel = kuerzel
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.plz = plz
        self.stadt = stadt

    def get_kuerzel(self):
        return self.kuerzel


# ToDo Klassen schicht, Urlaub, Krank als hierarchische Klassen vereinen schicht erbt von urlaub erbt von au
class Schicht:
    beginn = datetime
    end = datetime
    asn = ASN

    def __init__(self, beginn, ende, asn, original='root'):
        self.beginn = beginn
        self.ende = ende
        self.asn = asn
        self.original_schicht = original
        self.stundenzahl = self.berechne_stundenzahl()
        self.stundenlohn = lohntabelle.get_grundlohn(self.beginn)
        self.schichtlohn = self.stundenzahl * self.stundenlohn
        self.wechselschichtzulage = lohntabelle.get_zuschlag('Wechselschicht', beginn)
        self.wechselschichtzulage_schicht = self.wechselschichtzulage * self.stundenzahl
        self.nachtstunden = self.berechne_anzahl_nachtstunden()
        self.nachtzuschlag = lohntabelle.get_zuschlag('Nacht', beginn)
        self.nachtzuschlag_schicht = self.nachtstunden * self.nachtzuschlag
        self.zuschlaege = self.berechne_sa_so_weisil_feiertagszuschlaege()
        self.ist_kurzfristig = 0
        self.ist_ausfallgeld = 0
        self.ist_assistententreffen = 0
        self. ist_pcg = 0
        self.ist_schulung = 0

        if self.check_mehrtaegig() == 1:
            self.teilschichten = self.split_by_null_uhr()
        else:
            self.teilschichten = []

    def __str__(self):
        return self.asn.get_kuerzel() + " - " + self.beginn.strftime("%m/%d/%Y, %H:%M") + ' bis ' + \
               self.ende.strftime("%m/%d/%Y, %H:%M")

    def check_mehrtaegig(self):
        pseudoende = self.ende - datetime.timedelta(minutes=2)
        if self.beginn.strftime("%Y%m%d") == pseudoende.strftime("%Y%m%d"):
            return 0
        else:
            return 1

    def split_by_null_uhr(self):
        ausgabe = []
        if self.check_mehrtaegig() == 1:
            rest = dict(start=self.beginn, ende=self.ende)
            while rest['start'] <= rest['ende']:
                r_start = rest['start']
                neuer_start_rest_y = int(r_start.strftime('%Y'))
                neuer_start_rest_m = int(r_start.strftime('%m'))
                neuer_start_rest_d = int(r_start.strftime('%d'))
                neuer_start_rest = datetime.datetime(neuer_start_rest_y, neuer_start_rest_m, neuer_start_rest_d + 1)
                if neuer_start_rest <= rest['ende']:
                    ausgabe.append(Schicht(rest['start'],
                                           neuer_start_rest, self.asn, original=self.beginn.strftime('%Y%m%d%H%M')))
                else:
                    ausgabe.append(Schicht(rest['start'],
                                           rest['ende'], self.asn, original=self.beginn.strftime('%Y%m%d%H%M')))

                rest['start'] = neuer_start_rest
        else:
            ausgabe.append(self)

        return ausgabe

    def add_original_schicht(self, schicht):
        self.original_schicht = schicht

    def berechne_stundenzahl(self):
        diff = self.ende - self.beginn
        sekunden = diff.total_seconds()
        stunden = sekunden / 3600
        return stunden

    def berechne_anzahl_nachtstunden(self):
        nachtstunden = 0
        if self.check_mehrtaegig() == 1:
            teilschichten = self.split_by_null_uhr()
        else:
            teilschichten = [self]

        for teilschicht in teilschichten:
            beginn_jahr = int(teilschicht.beginn.strftime('%Y'))
            beginn_monat = int(teilschicht.beginn.strftime('%m'))
            beginn_tag = int(teilschicht.beginn.strftime('%d'))

            null_uhr = datetime.datetime(beginn_jahr, beginn_monat, beginn_tag, 0, 0, 0)
            sechs_uhr = datetime.datetime(beginn_jahr, beginn_monat, beginn_tag, 6, 0, 0)
            einundzwanzig_uhr = datetime.datetime(beginn_jahr, beginn_monat, beginn_tag, 21, 0, 0)

            # schicht beginnt zwischen 0 und 6 uhr
            if null_uhr <= teilschicht.beginn <= sechs_uhr:
                if teilschicht.ende <= sechs_uhr:
                    # schicht endet spätestens 6 uhr
                    nachtstunden += get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60

                elif sechs_uhr <= teilschicht.ende <= einundzwanzig_uhr:
                    # schicht endet nach 6 uhr aber vor 21 uhr
                    nachtstunden += get_duration(teilschicht.beginn, sechs_uhr, 'minutes') / 60

                else:
                    # schicht beginnt vor 6 uhr und geht über 21 Uhr hinaus
                    # das bedeutet ich ziehe von der kompletten schicht einfach die 15 Stunden Tagschicht ab.
                    # es bleibt der Nacht-Anteil
                    nachtstunden += get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60 - 15
            # schicht beginnt zwischen 6 und 21 uhr
            elif sechs_uhr <= teilschicht.beginn <= einundzwanzig_uhr:
                # fängt am tag an, geht aber bis in die nachtstunden
                if teilschicht.ende > einundzwanzig_uhr:
                    nachtstunden += get_duration(einundzwanzig_uhr, teilschicht.ende, 'minutes') / 60
            else:
                # schicht beginnt nach 21 uhr - die komplette schicht ist in der nacht
                nachtstunden += get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60
        return nachtstunden

    def berechne_sa_so_weisil_feiertagszuschlaege(self):
        feiertagsstunden = 0
        feiertagsstunden_steuerfrei = 0
        feiertagsstunden_steuerpflichtig = 0
        feiertagsarray = {}
        zuschlagsgrund = ''

        if self.check_feiertag() != '':
            if self.check_mehrtaegig() == 1:
                for teilschicht in self.teilschichten:
                    if teilschicht.check_feiertag() != '':
                        feiertagsstunden += teilschicht.berechne_stundenzahl
            else:
                feiertagsstunden = self.berechne_stundenzahl()

            zuschlag = lohntabelle.get_zuschlag(schichtdatum=self.beginn, zuschlag='Feiertag')
            feiertagsarray = {'zuschlagsgrund': 'Feiertag',
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': feiertagsstunden,
                              'stunden_steuerpflichtig': 0,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': feiertagsstunden * zuschlag,
                              'add_info': self.check_feiertag()
                              }
        elif self.beginn.weekday() == 6:
            feiertagsstunden = self.berechne_stundenzahl()
            zuschlag = lohntabelle.get_zuschlag(zuschlag='Sonntag', schichtdatum=self.beginn)
            feiertagsarray = {'zuschlagsgrund': 'Sonntag',
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': feiertagsstunden,
                              'stunden_steuerpflichtig': 0,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': feiertagsstunden * zuschlag,
                              'add_info': ''
                              }
        elif self.beginn.weekday() == 5:
            dreizehn_uhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 13, 0, 0)
            einundzwanzig_uhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 21, 0, 0)

            if self.beginn < dreizehn_uhr:
                if self.ende < dreizehn_uhr:
                    feiertagsstunden = 0
                elif dreizehn_uhr < self.ende <= einundzwanzig_uhr:
                    feiertagsstunden = get_duration(self.ende, dreizehn_uhr)
                else:  # self.ende > einundzwanzig_uhr:
                    feiertagsstunden = 8  # 21 - 13
            elif dreizehn_uhr <= self.beginn < einundzwanzig_uhr:
                if self.ende < einundzwanzig_uhr:
                    feiertagsstunden = self.berechne_stundenzahl()
                elif self.ende > einundzwanzig_uhr:
                    feiertagsstunden = get_duration(einundzwanzig_uhr, self.beginn)
            else:
                feiertagsstunden = 0

            zuschlag = lohntabelle.get_zuschlag(zuschlag='Samstag', schichtdatum=self.beginn)
            feiertagsarray = {'zuschlagsgrund': 'Samstag',
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': 0,
                              'stunden_steuerpflichtig': feiertagsstunden,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': float(feiertagsstunden) * zuschlag,
                              'add_info': '13:00 - 21:00 Uhr'
                              }
        elif datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                datetime.date(self.beginn.year, 12, 24) or \
                datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                datetime.date(self.beginn.year, 12, 24):
            if datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                    datetime.date(self.beginn.year, 12, 24):
                zuschlagsgrund = 'Heiligabend'
            if datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                    datetime.date(self.beginn.year, 12, 31):
                zuschlagsgrund = 'Silvester'

            sechsuhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 6, 0, 0)
            vierzehn_uhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 14, 0, 0)

            if self.beginn < sechsuhr:
                if self.ende <= sechsuhr:
                    feiertagsstunden_steuerfrei = feiertagsstunden_steuerpflichtig = 0
                elif sechsuhr < self.ende <= vierzehn_uhr:
                    feiertagsstunden_steuerpflichtig = get_duration(self.ende, sechsuhr, 'hours')
                    feiertagsstunden_steuerfrei = 0
                elif vierzehn_uhr < self.ende:
                    feiertagsstunden_steuerpflichtig = 8
                    feiertagsstunden_steuerfrei = get_duration(vierzehn_uhr, self.ende, 'hours')
            elif sechsuhr <= self.beginn:
                if self.ende <= vierzehn_uhr:
                    feiertagsstunden_steuerpflichtig = get_duration(self.ende, self.beginn, 'hours')
                    feiertagsstunden_steuerfrei = 0
                elif vierzehn_uhr < self.ende:
                    feiertagsstunden_steuerpflichtig = get_duration(vierzehn_uhr, self.beginn, 'hours')
                    feiertagsstunden_steuerfrei = get_duration(self.ende, vierzehn_uhr, 'hours')

            zuschlag = lohntabelle.get_zuschlag(zuschlag='WeiSil', schichtdatum=self.beginn)
            feiertagsstunden = feiertagsstunden_steuerfrei + feiertagsstunden_steuerpflichtig
            feiertagsarray = {'zuschlagsgrund': zuschlagsgrund,
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': feiertagsstunden_steuerfrei,
                              'stunden_steuerpflichtig': feiertagsstunden_steuerpflichtig,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': feiertagsstunden * zuschlag,
                              'add_info': '13:00 - 21:00 Uhr'
                              }
        return feiertagsarray

    def check_feiertag(self):
        jahr = self.beginn.year
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
                    'm': int(karfreitag.strftime('%d')), 'Y': 0}
        feiertage.append(feiertag)
        ostermontag = ostersonntag + datetime.timedelta(days=1)
        feiertag = {'name': 'Ostermontag', 'd': int(ostermontag.strftime('%d')),
                    'm': int(ostermontag.strftime('%d')), 'Y': 0}
        feiertage.append(feiertag)
        himmelfahrt = ostersonntag + datetime.timedelta(days=40)
        feiertag = {'name': 'Christi Himmelfahrt', 'd': int(himmelfahrt.strftime('%d')),
                    'm': int(himmelfahrt.strftime('%d')), 'Y': 0}
        feiertage.append(feiertag)
        pfingstsonntag = ostersonntag + datetime.timedelta(days=49)
        feiertag = {'name': 'Pfingstsonntag', 'd': int(pfingstsonntag.strftime('%d')),
                    'm': int(pfingstsonntag.strftime('%d')), 'Y': 0}
        feiertage.append(feiertag)
        pfingstmontag = ostersonntag + datetime.timedelta(days=50)
        feiertag = {'name': 'Pfingstmontag', 'd': int(pfingstmontag.strftime('%d')),
                    'm': int(pfingstmontag.strftime('%d')), 'Y': 0}
        feiertage.append(feiertag)
        ausgabe = ''
        for feiertag in feiertage:
            if feiertag['Y'] > 0:
                if feiertag['Y'] == self.beginn.year \
                        and self.beginn.day == feiertag['d'] \
                        and self.beginn.month == feiertag['m']:
                    ausgabe = feiertag['name']
                    break
            elif feiertag['Y'] == 0:
                if self.beginn.day == feiertag['d'] and self.beginn.month == feiertag['m']:
                    ausgabe = feiertag['name']
                    break
        return ausgabe

    @staticmethod
    def berechne_ostern(jahr):
        m = 0
        # Berechnung von Ostern mittels Gaußscher Osterformel
        # siehe http://www.ptb.de/de/org/4/44/441/oste.htm
        # mindestens bis 2031 richtig
        K = jahr / 100
        M = 15 + ((3 * K + 3) / 4) - ((8 * K + 13) / 25)
        S = 2 - ((3 * K + 3) / 4)
        A = jahr % 19
        D = (19 * A + M) % 30
        R = (D / 29) + ((D / 28) - (D / 29)) * (A / 11)
        OG = 21 + D - R
        SZ = 7 - (jahr + (jahr / 4) + S) % 7
        OE = 7 - ((OG - SZ) % 7)

        tmp = OG + OE  # das Osterdatum als Tages des März, also 32 entspricht 1. April
        if tmp > 31:  # Monat erhöhen, tmp=tag erniedriegen
            m = int(tmp / 31)
            tmp = int(round(tmp) - 31)
        return datetime.date(jahr, 3 + m, tmp)


class Urlaub:
    def __init__(self, beginn, ende, status='notiert'):
        self.beginn = beginn
        self.ende = ende
        # status 3 Möglichkeiten: notiert, beantragt, genehmigt
        self.status = status
        self.stundenzahl = self.berechne_durchschnittliche_stundenzahl_pro_tag()
        # todo Änderung des Stundensatzes während des Urlaubes
        self.ulohn_pro_stunde = lohntabelle.get_grundlohn(self.beginn)
        self.ulohn_pro_tag = self.stundenzahl * self.ulohn_pro_stunde

    def berechne_durchschnittliche_stundenzahl_pro_tag(self):
        # todo durchschnittliche Stundenzahl aus letzten ausgefüllten 6 Monaten
        return 6


class Arbeitsunfaehigkeit:
    def __init__(self, beginn, ende):
        self.beginn = beginn
        self.ende = ende

        self.stundenzahl = self.berechne_durchschnittliche_stundenzahl_pro_tag()
        # todo Änderung des Stundensatzes während des Urlaubes
        self.aulohn_pro_stunde = lohntabelle.get_grundlohn(self.beginn)
        self.aulohn_pro_tag = self.stundenzahl * self.aulohn_pro_stunde

    def berechne_durchschnittliche_stundenzahl_pro_tag(self):
        # todo durchschnittliche Stundenzahl aus letzten ausgefüllten 6 Monaten
        return 6


class LohnDatensatz:
    def __init__(self, erfahrungsstufe, grundlohn, zuschlaege):
        self.erfahrungsstufe = erfahrungsstufe
        self.eingruppierung = 5
        self.grundlohn = grundlohn
        self.zuschlaege = zuschlaege

    def get_grundlohn(self):
        return self.grundlohn

    def get_erfahrungsstufe(self):
        return self.erfahrungsstufe


class LohnTabelle:
    def __init__(self):
        # EG5 Erfahrungsstufen hinzufügen
        self.erfahrungsstufen = []
        self.zuschlaege = {'Nacht': 3.38, 'Samstag': 3.38, 'Sonntag': 4.22,
                           'Feiertag': 22.80, 'Wechselschicht': 0.63, 'WeiSil': 5.72, 'Überstunde': 4.48}
        self.erfahrungsstufen.append(LohnDatensatz(1, 14.92, self.zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(2, 16.18, self.zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(3, 16.89, self.zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.56, self.zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(5, 18.11, self.zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(6, 18.47, self.zuschlaege))

    def get_lohndatensatz_by_erfahrungsstufe(self, erfahrungsstufe):
        for datensatz in self.erfahrungsstufen:
            if datensatz.get_erfahrungsstufe() == erfahrungsstufe:
                return datensatz

    def get_grundlohn(self, datum):
        erfahrungsstufe = self.get_erfahrungsstufe(datum)
        ds = self.get_lohndatensatz_by_erfahrungsstufe(erfahrungsstufe)
        return ds.get_grundlohn()

    def get_zuschlag(self, zuschlag='all', schichtdatum=datetime.datetime.now()):
        erfahrungsstufe = self.get_erfahrungsstufe(schichtdatum)
        ds = self.get_lohndatensatz_by_erfahrungsstufe(erfahrungsstufe)
        if zuschlag == 'all':
            return ds.zuschlaege
        else:
            return ds.zuschlaege[zuschlag]

    @staticmethod
    def get_erfahrungsstufe(datum=datetime.datetime.now()):
        delta = get_duration(assistent.einstellungsdatum, datum, 'years')
        # einstieg mit 1
        # nach 1 Jahr insgesamt 2
        # nach 3 jahren insgesamt 3
        # nach 6 jahren insg. 4
        # nach 10 Jahren insg. 5
        # nach 15 Jahren insg. 6
        if delta == 0:
            return 1
        elif 1 <= delta < 3:
            return 2
        elif 3 <= delta < 6:
            return 3
        elif 6 <= delta < 10:
            return 4
        elif 10 <= delta < 15:
            return 5
        else:
            return 6


def end_of_month(month, year):
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return datetime.date(year, month, 1) - datetime.timedelta(days=1)


def get_duration(then, now=datetime.datetime.now(), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(secs=None):
        return divmod(secs if secs is not None else duration_in_s, 86400)  # Seconds in a day = 86400

    def hours(secs=None):
        return divmod(secs if secs is not None else duration_in_s, 3600)  # Seconds in an hour = 3600

    def minutes(secs=None):
        return divmod(secs if secs is not None else duration_in_s, 60)  # Seconds in a minute = 60

    def seconds(secs=None):
        if secs is not None:
            return divmod(secs, 1)
        return duration_in_s

    def total_duration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]),
                                                                                                   int(h[0]), int(m[0]),
                                                                                                   int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': total_duration()
    }[interval]


def sort_und_berechne_schichten_by_day(schichten, monatjahr=datetime.date.today()):
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


def neuer_as():
    def action_save_neuer_as():
        global assistent
        einstellungsdatum_date_obj = datetime.datetime.strptime(form_neuer_as_einstellungsdatum_input.get_date(),
                                                                '%m/%d/%y')
        assistent = AS(form_neuer_as_nachname_input.get(), form_neuer_as_vorname_input.get(),
                       form_neuer_as_email_input.get(), einstellungsdatum_date_obj)
        assistent.__class__.assistent_is_loaded = 1
        alles_speichern(neu=1)
        fenster_neuer_as.destroy()

    #  global assistent
    fenster_neuer_as = tk.Toplevel(fenster)
    form_neuer_as_headline = tk.Label(fenster_neuer_as, text="Wer bist du denn eigentlich?")
    form_neuer_as_vorname_label = tk.Label(fenster_neuer_as, text="Vorname")
    form_neuer_as_vorname_input = tk.Entry(fenster_neuer_as, bd=5, width=40)
    form_neuer_as_nachname_label = tk.Label(fenster_neuer_as, text="Nachname")
    form_neuer_as_nachname_input = tk.Entry(fenster_neuer_as, bd=5, width=40)
    form_neuer_as_email_label = tk.Label(fenster_neuer_as, text="Email")
    form_neuer_as_email_input = tk.Entry(fenster_neuer_as, bd=5, width=40)
    form_neuer_as_einstellungsdatum_label = tk.Label(fenster_neuer_as, text="Seit wann bei ad? (tt.mm.JJJJ)")
    form_neuer_as_einstellungsdatum_input = Calendar(fenster_neuer_as)
    form_neuer_as_save_button = tk.Button(fenster_neuer_as, text="Daten speichern", command=action_save_neuer_as)
    form_neuer_as_exit_button = tk.Button(fenster_neuer_as, text="Abbrechen", command=fenster_neuer_as.destroy)

    # ins Fenster packen
    form_neuer_as_headline.grid(row=0, column=0, columnspan=2)
    form_neuer_as_vorname_label.grid(row=1, column=0)
    form_neuer_as_vorname_input.grid(row=1, column=1)
    form_neuer_as_nachname_label.grid(row=2, column=0)
    form_neuer_as_nachname_input.grid(row=2, column=1)
    form_neuer_as_email_label.grid(row=3, column=0)
    form_neuer_as_email_input.grid(row=3, column=1)
    # TODO Text nach oben
    form_neuer_as_einstellungsdatum_label.grid(row=4, column=0)
    form_neuer_as_einstellungsdatum_input.grid(row=4, column=1)
    form_neuer_as_exit_button.grid(row=5, column=0)
    form_neuer_as_save_button.grid(row=5, column=1)


def neue_schicht():
    # TODO allgemeine show-hide funktion
    def tag_nacht_reise(value, label, button):
        if value == 3:
            label.grid()
            button.grid()
        elif value == 1 or value == 2:
            label.grid_remove()
            button.grid_remove()

    def neuer_asn(value):
        if value == "Neuer ASN":
            form_neuer_asn_kuerzel_label.grid(row=6, column=0)
            form_neuer_asn_kuerzel_input.grid(row=6, column=1)
            form_neuer_asn_vorname_label.grid(row=7, column=0)
            form_neuer_asn_vorname_input.grid(row=7, column=1)
            form_neuer_asn_nachname_label.grid(row=8, column=0)
            form_neuer_asn_nachname_input.grid(row=8, column=1)
            form_neuer_asn_strasse_label.grid(row=9, column=0)
            form_neuer_asn_strasse_input.grid(row=9, column=1)
            form_neuer_asn_hausnummer_input.grid(row=9, column=2)
            form_neuer_asn_plz_label.grid(row=10, column=0)
            form_neuer_asn_plz_input.grid(row=10, column=1)
            form_neuer_asn_stadt_label.grid(row=11, column=0)
            form_neuer_asn_stadt_input.grid(row=11, column=1)
        else:
            form_neuer_asn_kuerzel_label.grid_remove()
            form_neuer_asn_kuerzel_input.grid_remove()
            form_neuer_asn_vorname_label.grid_remove()
            form_neuer_asn_vorname_input.grid_remove()
            form_neuer_asn_nachname_label.grid_remove()
            form_neuer_asn_nachname_input.grid_remove()
            form_neuer_asn_strasse_label.grid_remove()
            form_neuer_asn_strasse_input.grid_remove()
            form_neuer_asn_hausnummer_input.grid_remove()
            form_neuer_asn_plz_label.grid_remove()
            form_neuer_asn_plz_input.grid_remove()
            form_neuer_asn_stadt_label.grid_remove()
            form_neuer_asn_stadt_input.grid_remove()

    def action_save_neue_schicht(undneu=0):
        global assistent

        startdatum = form_neue_schicht_startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                   int(form_neue_schicht_startzeit_input.hourstr.get()),
                                   int(form_neue_schicht_startzeit_input.minstr.get()))

        # ende der Schicht bestimmen. Fälle: Tagschicht, Nachtschicht, Reise
        # todo minstring darf nicht mehr als 59 sein. kann durch ungeduldiges tippen passieren entry validieren
        if fenster_neue_schicht.v.get() == 1:  # Tagschicht
            ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                     int(form_neue_schicht_endzeit_input.hourstr.get()),
                                     int(form_neue_schicht_endzeit_input.minstr.get()))
        elif fenster_neue_schicht.v.get() == 2:  # Nachtschicht
            ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]) + 1,
                                     int(form_neue_schicht_endzeit_input.hourstr.get()),
                                     int(form_neue_schicht_endzeit_input.minstr.get()))
        else:  # Reisebegleitung
            enddatum = form_neue_schicht_enddatum_input.get_date().split('/')
            ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]),
                                     int(form_neue_schicht_endzeit_input.hourstr.get()),
                                     int(form_neue_schicht_endzeit_input.minstr.get()))
        if variable.get() == "Neuer ASN":
            asn = ASN(form_neuer_asn_nachname_input.get(),
                      form_neuer_asn_vorname_input.get(),
                      form_neuer_asn_kuerzel_input.get()
                      )
            assistent.asn_dazu(asn)
        else:
            asn = assistent.get_asn_by_kuerzel(variable.get())
        # Schicht erstellen und zum Assistenten stopfen
        schicht = Schicht(beginn, ende, asn)
        assistent.schicht_dazu(schicht)
        alles_speichern()
        fenster_neue_schicht.destroy()
        if undneu == 1:
            neue_schicht()

    fenster_neue_schicht = tk.Toplevel(fenster)
    form_neue_schicht_headline = tk.Label(fenster_neue_schicht, text="Schichten eintragen")
    form_neue_schicht_startdatum_label = tk.Label(fenster_neue_schicht, text="Datum (Beginn) der Schicht")
    form_neue_schicht_startdatum_input = Calendar(fenster_neue_schicht, date_pattern='MM/dd/yyyy')
    form_neue_schicht_startzeit_label = tk.Label(fenster_neue_schicht, text="Startzeit")
    form_neue_schicht_startzeit_input = TimePicker(fenster_neue_schicht)
    form_neue_schicht_endzeit_label = tk.Label(fenster_neue_schicht, text="Schichtende")
    form_neue_schicht_endzeit_input = TimePicker(fenster_neue_schicht)
    form_neue_schicht_enddatum_label = tk.Label(fenster_neue_schicht, text="Datum Ende der Schicht")
    form_neue_schicht_enddatum_input = Calendar(fenster_neue_schicht, date_pattern='MM/dd/yyyy')
    # TODO Vorauswahl konfigurieren lassen
    fenster_neue_schicht.v = tk.IntVar()
    fenster_neue_schicht.v.set(1)
    form_neue_schicht_anderes_enddatum_label = tk.Label(fenster_neue_schicht,
                                                        text="Tagschicht, Nachtschicht\noder mehrtägig?")
    form_neue_schicht_anderes_enddatum_input_radio1 = \
        tk.Radiobutton(fenster_neue_schicht, text="Tagschicht", padx=20,
                       variable=fenster_neue_schicht.v, value=1,
                       command=lambda: tag_nacht_reise(1, form_neue_schicht_enddatum_input,
                                                       form_neue_schicht_enddatum_label))
    form_neue_schicht_anderes_enddatum_input_radio2 = \
        tk.Radiobutton(fenster_neue_schicht, text="Nachtschicht\n(Ende der Schicht ist am Folgetag)", padx=20,
                       variable=fenster_neue_schicht.v, value=2,
                       command=lambda: tag_nacht_reise(2, form_neue_schicht_enddatum_input,
                                                       form_neue_schicht_enddatum_label))
    form_neue_schicht_anderes_enddatum_input_radio3 = \
        tk.Radiobutton(fenster_neue_schicht, text="Mehrtägig/Reisebegleitung", padx=20,
                       variable=fenster_neue_schicht.v, value=3,
                       command=lambda: tag_nacht_reise(3, form_neue_schicht_enddatum_input,
                                                       form_neue_schicht_enddatum_label))
    form_neue_schicht_asn_label = tk.Label(fenster_neue_schicht, text="Assistenznehmer")
    # grundsätzliche Optionen für Dropdown
    option_list = ["Bitte auswählen", "Neuer ASN", *assistent.get_all_asn()]

    variable = tk.StringVar()
    variable.set(option_list[0])
    form_neue_schicht_asn_dropdown = tk.OptionMenu(fenster_neue_schicht, variable, *option_list, command=neuer_asn)
    # Felder für neuen ASN
    form_neuer_asn_kuerzel_label = tk.Label(fenster_neue_schicht, text="Kürzel")
    form_neuer_asn_kuerzel_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neuer_asn_vorname_label = tk.Label(fenster_neue_schicht, text="Vorname")
    form_neuer_asn_vorname_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neuer_asn_nachname_label = tk.Label(fenster_neue_schicht, text="Nachname")
    form_neuer_asn_nachname_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neuer_asn_strasse_label = tk.Label(fenster_neue_schicht, text="Straße/Hausnummer")
    form_neuer_asn_strasse_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neuer_asn_hausnummer_input = tk.Entry(fenster_neue_schicht, bd=5, width=10)
    form_neuer_asn_plz_label = tk.Label(fenster_neue_schicht, text="Postleitzahl")
    form_neuer_asn_plz_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neuer_asn_stadt_label = tk.Label(fenster_neue_schicht, text="Stadt")
    form_neuer_asn_stadt_input = tk.Entry(fenster_neue_schicht, bd=5, width=40)
    form_neue_schicht_save_button = tk.Button(fenster_neue_schicht, text="Daten speichern",
                                              command=action_save_neue_schicht)
    form_neue_schicht_exit_button = tk.Button(fenster_neue_schicht, text="Abbrechen",
                                              command=fenster_neue_schicht.destroy)
    form_neue_schicht_saveandnew_button = tk.Button(fenster_neue_schicht, text="Daten speichern und neu",
                                                    command=lambda: action_save_neue_schicht(undneu=1))

    # TODO Berücksichtigen PCG, AT, Büro, Ausfallgeld, fester ASN, regelmäßige Schicht, besonderer Einsatz

    # ins Fenster packen
    form_neue_schicht_headline.grid(row=0, column=0, columnspan=4)
    form_neue_schicht_startdatum_label.grid(row=1, column=0)
    form_neue_schicht_startdatum_input.grid(row=1, column=1, columnspan=2)
    form_neue_schicht_enddatum_label.grid(row=1, column=3)
    form_neue_schicht_enddatum_input.grid(row=1, column=4)
    form_neue_schicht_startzeit_label.grid(row=2, column=0)
    form_neue_schicht_startzeit_input.grid(row=2, column=1)
    form_neue_schicht_endzeit_label.grid(row=2, column=2)
    form_neue_schicht_endzeit_input.grid(row=2, column=3)
    # TODO prüfen, wenn endzeit < startzeit nachtschicht im Radiobutton markieren
    form_neue_schicht_anderes_enddatum_label.grid(row=3, column=0)
    # TODO zusätzliche Felder für Reisen

    form_neue_schicht_anderes_enddatum_input_radio1.grid(row=3, column=1)
    form_neue_schicht_anderes_enddatum_input_radio2.grid(row=3, column=2)
    form_neue_schicht_anderes_enddatum_input_radio3.grid(row=3, column=3)
    # TODO alternativer Ort für Dienstbeginn und Ende
    # TODO BSD
    # TODO HACK besser machen? zwingt enddatum auf invisible
    tag_nacht_reise(1, form_neue_schicht_enddatum_input,
                    form_neue_schicht_enddatum_label)
    form_neue_schicht_asn_label.grid(row=5, column=0)
    form_neue_schicht_asn_dropdown.grid(row=5, column=1)
    form_neue_schicht_save_button.grid(row=15, column=0)
    form_neue_schicht_exit_button.grid(row=15, column=1)
    form_neue_schicht_saveandnew_button.grid(row=15, column=2)


def neuer_urlaub():
    # TODO allgemeine show-hide funktion

    def action_save_neuer_urlaub(undneu=0):
        global assistent

        startdatum = form_neuer_urlaub_startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = form_neuer_urlaub_enddatum_input.get_date().split('/')
        # urlaub geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)
        status = fenster_neuer_urlaub.urlaubsstatus.get()

        # Schicht erstellen und zum Assistenten stopfen
        urlaub = Urlaub(beginn, ende, status)
        assistent.urlaub_dazu(urlaub)
        alles_speichern()
        fenster_neuer_urlaub.destroy()
        if undneu == 1:
            neuer_urlaub()

    fenster_neuer_urlaub = tk.Toplevel(fenster)
    form_neuer_urlaub_headline = tk.Label(fenster_neuer_urlaub, text="Urlaub eintragen")
    form_neuer_urlaub_startdatum_label = tk.Label(fenster_neuer_urlaub, text="von")
    form_neuer_urlaub_startdatum_input = Calendar(fenster_neuer_urlaub, date_pattern='MM/dd/yyyy')
    form_neuer_urlaub_enddatum_label = tk.Label(fenster_neuer_urlaub, text="bis")
    form_neuer_urlaub_enddatum_input = Calendar(fenster_neuer_urlaub, date_pattern='MM/dd/yyyy')
    fenster_neuer_urlaub.urlaubsstatus = tk.StringVar()
    fenster_neuer_urlaub.urlaubsstatus.set('notiert')
    form_neuer_urlaub_status_label = tk.Label(fenster_neuer_urlaub, text="Status")
    form_neuer_urlaub_status_input_radio1 = \
        tk.Radiobutton(fenster_neuer_urlaub, text="notiert", padx=20,
                       variable=fenster_neuer_urlaub.urlaubsstatus, value='notiert')
    form_neuer_urlaub_status_input_radio2 = \
        tk.Radiobutton(fenster_neuer_urlaub, text="beantragt", padx=20,
                       variable=fenster_neuer_urlaub.urlaubsstatus, value='beantragt')
    form_neuer_urlaub_status_input_radio3 = \
        tk.Radiobutton(fenster_neuer_urlaub, text="genehmigt", padx=20,
                       variable=fenster_neuer_urlaub.urlaubsstatus, value='genehmigt')

    form_neuer_urlaub_save_button = tk.Button(fenster_neuer_urlaub, text="Daten speichern",
                                              command=action_save_neuer_urlaub)
    form_neuer_urlaub_exit_button = tk.Button(fenster_neuer_urlaub, text="Abbrechen",
                                              command=fenster_neuer_urlaub.destroy)
    form_neuer_urlaub_saveandnew_button = tk.Button(fenster_neuer_urlaub, text="Daten speichern und neu",
                                                    command=lambda: action_save_neuer_urlaub(undneu=1))

    # TODO Berücksichtigen PCG, AT, Büro, Ausfallgeld, fester ASN, regelmäßige Schicht, besonderer Einsatz

    # ins Fenster packen
    form_neuer_urlaub_headline.grid(row=0, column=0, columnspan=4)
    form_neuer_urlaub_startdatum_label.grid(row=1, column=0)
    form_neuer_urlaub_startdatum_input.grid(row=1, column=1, columnspan=2)
    form_neuer_urlaub_enddatum_label.grid(row=1, column=3)
    form_neuer_urlaub_enddatum_input.grid(row=1, column=4)

    form_neuer_urlaub_status_label.grid(row=3, column=0)

    form_neuer_urlaub_status_input_radio1.grid(row=3, column=1)
    form_neuer_urlaub_status_input_radio2.grid(row=3, column=2)
    form_neuer_urlaub_status_input_radio3.grid(row=3, column=3)

    form_neuer_urlaub_save_button.grid(row=15, column=0)
    form_neuer_urlaub_exit_button.grid(row=15, column=1)
    form_neuer_urlaub_saveandnew_button.grid(row=15, column=2)


def neue_arbeitsunfaehigkeit():
    # TODO allgemeine show-hide funktion

    def action_save_neue_arbeitsunfaehigkeit(undneu=0):
        global assistent

        startdatum = form_neue_arbeitsunfaehigkeit_startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = form_neue_arbeitsunfaehigkeit_enddatum_input.get_date().split('/')
        # urlaub geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)
        status = fenster_neue_arbeitsunfaehigkeit.urlaubsstatus.get()

        # Schicht erstellen und zum Assistenten stopfen
        au = Arbeitsunfaehigkeit(beginn, ende, status)
        assistent.au_dazu(au)
        alles_speichern()
        fenster_neue_arbeitsunfaehigkeit.destroy()
        if undneu == 1:
            neue_arbeitsunfaehigkeit()

    fenster_neue_arbeitsunfaehigkeit = tk.Toplevel(fenster)
    form_neue_arbeitsunfaehigkeit_headline = tk.Label(fenster_neue_arbeitsunfaehigkeit, text="AU/krank eintragen")
    form_neue_arbeitsunfaehigkeit_startdatum_label = tk.Label(fenster_neue_arbeitsunfaehigkeit, text="von")
    form_neue_arbeitsunfaehigkeit_startdatum_input = Calendar(fenster_neue_arbeitsunfaehigkeit,
                                                              date_pattern='MM/dd/yyyy')
    form_neue_arbeitsunfaehigkeit_enddatum_label = tk.Label(fenster_neue_arbeitsunfaehigkeit, text="bis")
    form_neue_arbeitsunfaehigkeit_enddatum_input = Calendar(fenster_neue_arbeitsunfaehigkeit, date_pattern='MM/dd/yyyy')
    fenster_neue_arbeitsunfaehigkeit.urlaubsstatus = tk.StringVar()
    fenster_neue_arbeitsunfaehigkeit.urlaubsstatus.set('notiert')

    form_neue_arbeitsunfaehigkeit_save_button = tk.Button(fenster_neue_arbeitsunfaehigkeit, text="Daten speichern",
                                                          command=action_save_neue_arbeitsunfaehigkeit)
    form_neue_arbeitsunfaehigkeit_exit_button = tk.Button(fenster_neue_arbeitsunfaehigkeit, text="Abbrechen",
                                                          command=fenster_neue_arbeitsunfaehigkeit.destroy)
    form_neue_arbeitsunfaehigkeit_saveandnew_button = tk.Button(fenster_neue_arbeitsunfaehigkeit,
                                                                text="Daten speichern und neu",
                                                                command=lambda: action_save_neue_arbeitsunfaehigkeit(
                                                                    undneu=1))

    # TODO Berücksichtigen PCG, AT, Büro, Ausfallgeld, fester ASN, regelmäßige Schicht, besonderer Einsatz

    # ins Fenster packen
    form_neue_arbeitsunfaehigkeit_headline.grid(row=0, column=0, columnspan=4)
    form_neue_arbeitsunfaehigkeit_startdatum_label.grid(row=1, column=0)
    form_neue_arbeitsunfaehigkeit_startdatum_input.grid(row=1, column=1, columnspan=2)
    form_neue_arbeitsunfaehigkeit_enddatum_label.grid(row=1, column=3)
    form_neue_arbeitsunfaehigkeit_enddatum_input.grid(row=1, column=4)

    form_neue_arbeitsunfaehigkeit_save_button.grid(row=15, column=0)
    form_neue_arbeitsunfaehigkeit_exit_button.grid(row=15, column=1)
    form_neue_arbeitsunfaehigkeit_saveandnew_button.grid(row=15, column=2)


def alles_speichern(neu=0):
    global assistent
    # TODO File picker

    if neu == 1:
        files = [('Assistenten-Dateien', '*.dat')]
        dateiname = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        dateiname = dateiname.name
        assistent.set_filepath(dateiname)
        assistent.__class__.assistent_is_loaded = 1
    else:
        dateiname = assistent.get_filepath()
    outfile = open(dateiname, 'wb')
    pickle.dump(assistent, outfile)
    outfile.close()
    if neu == 1:
        zeichne_hauptmenue()
    zeichne_hauptseite()


def alles_laden():
    files = [('Assistenten-Dateien', '*.dat')]
    dateiname = filedialog.askopenfilename(filetypes=files, defaultextension=files)
    if not dateiname == '':
        global assistent
        assistent.set_filepath(dateiname)
        infile = open(dateiname, 'rb')
        assistent = pickle.load(infile)
        infile.close()
        assistent.__class__.assistent_is_loaded = 1
        zeichne_hauptmenue()
        zeichne_hauptseite()


def action_get_info_dialog():
    m_text = "\
************************\n\
Autor: Simon Beyer\n\
Date: 16.11.2020\n\
Version: 0.01\n\
************************"
    tk.messagebox.showinfo(message=m_text, title="Infos")


def zeichne_hauptmenue():
    # Menüleiste erstellen
    menuleiste = tk.Menu(root)

    # Menü Datei und Help erstellen
    datei_menu = tk.Menu(menuleiste, tearoff=0)
    bearbeiten_menu = tk.Menu(menuleiste, tearoff=0)
    help_menu = tk.Menu(menuleiste, tearoff=0)

    # Beim Klick auf Datei oder auf Help sollen nun weitere Einträge erscheinen.
    # Diese werden also zu "datei_menu" und "help_menu" hinzugefügt
    datei_menu.add_command(label="Neue Assistenten-Datei", command=neuer_as)
    datei_menu.add_command(label="Assistenten-Datei laden", command=alles_laden)
    datei_menu.add_command(label="Assistenten-Datei speichern", command=alles_speichern)
    datei_menu.add_command(label="Assistenten-Datei speichern unter")
    datei_menu.add_separator()  # Fügt eine Trennlinie hinzu
    datei_menu.add_command(label="Exit", command=fenster.quit)

    bearbeiten_menu.add_command(label="Schicht eintragen", command=neue_schicht)
    bearbeiten_menu.add_command(label="Urlaub eintragen", command=neuer_urlaub)
    bearbeiten_menu.add_command(label="AU/krank eintragen", command=neue_arbeitsunfaehigkeit)

    help_menu.add_command(label="Info!", command=action_get_info_dialog)

    # Nun fügen wir die Menüs (Datei und Help) der Menüleiste als
    # "Drop-Down-Menü" hinzu
    menuleiste.add_cascade(label="Datei", menu=datei_menu)
    menuleiste.add_cascade(label="Bearbeiten", menu=bearbeiten_menu)
    menuleiste.add_cascade(label="Help", menu=help_menu)
    # Die Menüleiste mit den Menüeinträgen noch dem Fenster übergeben und fertig.
    root.config(menu=menuleiste)


def split_schichten_um_mitternacht(schichten):
    ausgabe = []
    for schicht in schichten.values():
        if not schicht.teilschichten:
            ausgabe.append(schicht)
        else:
            for teilschicht in schicht.teilschichten:
                ausgabe.append(teilschicht)
    return ausgabe


def kill_schicht(key):
    assistent.delete_schicht(key=key)
    zeichne_hauptseite()


def zeichne_hauptseite():
    global button_neu, button_oeffnen, assistent

    def erstelle_navigation(offset=0):
        def monat_zurueck(offs):
            offs -= 1
            erstelle_navigation(offs)
            erstelle_tabelle(offs)
            erstelle_seitenleiste()

        def monat_vor(offs):
            offs += 1
            erstelle_navigation(offs)
            erstelle_tabelle(offs)
            erstelle_seitenleiste()

        for navwidget in nav.winfo_children():
            navwidget.destroy()

        # offset = 0
        vormonat = tk.Button(nav, text='einen Monat Zurück', command=lambda: monat_zurueck(offset))
        aktuelles_datum = datetime.date.today()
        jahrmonat = divmod(int(aktuelles_datum.strftime('%m')) + offset, 12)
        jahroffset = jahrmonat[0]
        monat = jahrmonat[1]
        if monat == 0:
            monat = 12
        arbeitsdate = datetime.date(int(aktuelles_datum.strftime('%Y')) + jahroffset, monat, 1)
        aktueller_monat = tk.Label(nav, text=arbeitsdate.strftime("%B %Y"))
        naechster_monat = tk.Button(nav, text='Nächster Monat', command=lambda: monat_vor(offset))

        # in den frame packen
        vormonat.grid(row=0, column=0)
        aktueller_monat.grid(row=0, column=1)
        naechster_monat.grid(row=0, column=2)

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

    def erstelle_tabelle(offs=0):
        command = text = zelle = image = ''
        for tabwidget in tabelle.winfo_children():
            tabwidget.destroy()

        zuschlaege = {}
        for zuschlag_name in lohntabelle.zuschlaege.keys():
            zuschlaege[zuschlag_name] = {
                'stunden_gesamt': 0,
                'zuschlaege_gesamt': 0,
                'stunden_steuerfrei': 0,
                'stunden_steuerpflichtig': 0,
                'zuschlag_pro_stunde': 0,
            }

        tabelle.summen = {'arbeitsstunden': 0,
                          'grundlohn': 0,
                          'grundlohn_pro_stunde': 0,
                          'nachtstunden': 0,
                          'nachtzuschlag': 0,
                          'nachtzuschlag_pro_stunde': 0,
                          'wechselschichtzulage': 0,
                          'wechselschichtzulage_pro_stunde': 0,
                          'zuschlaege': zuschlaege
                          }

        arbeitsdatum = start = verschiebe_monate(offs)
        end = verschiebe_monate(1, arbeitsdatum)
        schichten = assistent.get_all_schichten(start, end)
        schichten_sortiert = split_schichten_um_mitternacht(schichten)
        schichten_sortiert = sort_und_berechne_schichten_by_day(schichten_sortiert, arbeitsdatum)

        # Tabelle aufbauen
        # kopfzeile erstellen
        tk.Label(tabelle, text='Tag', borderwidth=1, relief="solid", width=6).grid(row=0, column=10, columnspan=2)
        tk.Label(tabelle, text='von', borderwidth=1, relief="solid", width=5).grid(row=0, column=12)
        tk.Label(tabelle, text='bis', borderwidth=1, relief="solid", width=5).grid(row=0, column=13)
        tk.Label(tabelle, text='ASN', borderwidth=1, relief="solid", width=8).grid(row=0, column=14)
        tk.Label(tabelle, text='Std', borderwidth=1, relief="solid", width=5).grid(row=0, column=15)
        tk.Label(tabelle, text='Grundlohn', borderwidth=1, relief="solid", width=8).grid(row=0, column=16)
        tk.Label(tabelle, text='NachtStd', borderwidth=1, relief="solid", width=8).grid(row=0, column=17)
        tk.Label(tabelle, text='Nachtzu.', borderwidth=1, relief="solid", width=8).grid(row=0, column=18)
        tk.Label(tabelle, text='Zuschlaege', borderwidth=1, relief="solid", width=18).grid(row=0, column=19,
                                                                                           columnspan=2)
        tk.Label(tabelle, text='Wechsel', borderwidth=1, relief="solid", width=8).grid(row=0, column=21)

        # körper
        meine_tabelle = []
        spaltenzahl = 22
        zaehler = 0
        width = 0
        inhalt = ''
        for zeilendaten in schichten_sortiert:
            zeile = []
            zaehler += 1
            for spaltennummer in range(0, spaltenzahl):
                if spaltennummer == 0:
                    # Creating a photoimage object to use image
                    image = "images/edit.png"
                    text = 'edit'
                    command = 'edit'

                elif spaltennummer == 1:
                    text = 'del'
                    command = 'kill'
                    if zeilendaten[1] != 'empty':
                        if zeilendaten[1].original_schicht != "root":
                            key_string = zeilendaten[1].original_schicht
                        else:
                            key_string = zeilendaten[1].beginn.strftime('%Y%m%d%H%M')
                    image = "images/del.png"

                elif 1 < spaltennummer < 10:
                    text = ''

                elif spaltennummer == 10:
                    zeile = []
                    width = 4
                    # TODO timezone checken
                    inhalt = datetime.datetime(arbeitsdatum.year, arbeitsdatum.month, zeilendaten[0]).strftime('%a')

                elif spaltennummer == 11:
                    zeile = []
                    width = 3
                    inhalt = zeilendaten[0]
                elif spaltennummer == 12:
                    if zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].beginn.strftime('%H:%M')
                    else:
                        inhalt = ''
                    width = 5
                elif spaltennummer == 13:
                    if zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].ende.strftime('%H:%M')
                    else:
                        inhalt = ''
                    width = 5

                elif spaltennummer == 14:
                    if assistent.check_au(datetime.datetime(arbeitsdatum.year,
                                                            arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        inhalt = 'AU'
                    elif assistent.check_urlaub(datetime.datetime(arbeitsdatum.year,
                                                                  arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        inhalt = 'Urlaub'
                    elif zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].asn.kuerzel
                    else:
                        inhalt = ''
                    width = 10

                elif spaltennummer == 15:
                    if assistent.check_au(datetime.datetime(arbeitsdatum.year,
                                                            arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        au = assistent.check_au(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                  zeilendaten[0], 0, 1))
                        austunden = au.berechne_durchschnittliche_stundenzahl_pro_tag()
                        inhalt = austunden
                        tabelle.summen['arbeitsstunden'] += austunden
                    elif assistent.check_urlaub(datetime.datetime(arbeitsdatum.year,
                                                                  arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        urlaub = assistent.check_urlaub(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                          zeilendaten[0], 0, 1))
                        ustunden = urlaub.berechne_durchschnittliche_stundenzahl_pro_tag()
                        inhalt = ustunden
                        tabelle.summen['arbeitsstunden'] += ustunden
                    elif zeilendaten[1] != 'empty':
                        tabelle.summen['arbeitsstunden'] += zeilendaten[1].stundenzahl
                        inhalt = str(zeilendaten[1].berechne_stundenzahl())
                    else:
                        inhalt = ''
                    width = 5
                elif spaltennummer == 16:
                    if assistent.check_au(datetime.datetime(arbeitsdatum.year,
                                                                arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        urlaub = assistent.check_au(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                          zeilendaten[0], 0, 1))
                        aulohn = au.aulohn_pro_tag
                        aulohn_pro_stunde = au.aulohn_pro_stunde
                        tabelle.summen['grundlohn'] += aulohn
                        tabelle.summen['grundlohn_pro_stunde'] = aulohn_pro_stunde
                        inhalt = "{:,.2f}€".format(aulohn)
                    elif assistent.check_urlaub(datetime.datetime(arbeitsdatum.year,
                                                                arbeitsdatum.month, zeilendaten[0], 0, 1)):
                        urlaub = assistent.check_urlaub(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                          zeilendaten[0], 0, 1))
                        ulohn = urlaub.ulohn_pro_tag
                        ulohn_pro_stunde = urlaub.ulohn_pro_stunde
                        tabelle.summen['grundlohn'] += ulohn
                        tabelle.summen['grundlohn_pro_stunde'] = ulohn_pro_stunde
                        inhalt = "{:,.2f}€".format(ulohn)
                    elif zeilendaten[1] != 'empty':
                        schichtlohn = zeilendaten[1].schichtlohn
                        tabelle.summen['grundlohn'] += zeilendaten[1].schichtlohn
                        tabelle.summen['grundlohn_pro_stunde'] = zeilendaten[1].stundenlohn
                        inhalt = "{:,.2f}€".format(schichtlohn)
                    else:
                        inhalt = ''
                    width = 8
                elif spaltennummer == 17:
                    if zeilendaten[1] != 'empty':
                        nachtstunden = zeilendaten[1].nachtstunden
                        tabelle.summen['nachtstunden'] += nachtstunden
                        inhalt = str(nachtstunden)
                    else:
                        inhalt = ''
                    width = 8
                elif spaltennummer == 18:
                    if zeilendaten[1] != 'empty':
                        nachtzuschlag_schicht = zeilendaten[1].nachtzuschlag_schicht
                        tabelle.summen['nachtzuschlag'] += zeilendaten[1].nachtzuschlag_schicht
                        tabelle.summen['nachtzuschlag_pro_stunde'] = zeilendaten[1].nachtzuschlag
                        inhalt = "{:,.2f}€".format(nachtzuschlag_schicht)
                    else:
                        inhalt = ''
                    width = 8
                elif spaltennummer == 19:
                    if zeilendaten[1] != 'empty' and zeilendaten[1].zuschlaege != {}:
                        grund = zeilendaten[1].zuschlaege['zuschlagsgrund']
                        zuschlag_stunden = zeilendaten[1].zuschlaege['stunden_gesamt']
                        tabelle.summen['zuschlaege'][grund]['stunden_gesamt'] \
                            += zuschlag_stunden
                        inhalt = str(zuschlag_stunden) + ' ' + zeilendaten[1].zuschlaege['zuschlagsgrund']
                    else:
                        inhalt = ''
                    width = 15
                elif spaltennummer == 20:
                    if zeilendaten[1] != 'empty' and zeilendaten[1].zuschlaege != {}:
                        grund = zeilendaten[1].zuschlaege['zuschlagsgrund']
                        zuschlag_schicht = zeilendaten[1].zuschlaege['zuschlag_schicht']
                        tabelle.summen['zuschlaege'][grund]['zuschlaege_gesamt'] \
                            += zuschlag_schicht
                        tabelle.summen['zuschlaege'][grund]['zuschlag_pro_stunde'] = \
                            zeilendaten[1].zuschlaege['zuschlag_pro_stunde']
                        inhalt = "{:,.2f}€".format(zuschlag_schicht)
                    else:
                        inhalt = ''
                    width = 8
                elif spaltennummer == 21:
                    if zeilendaten[1] != 'empty':
                        tabelle.summen['wechselschichtzulage'] += zeilendaten[1].wechselschichtzulage_schicht
                        tabelle.summen['wechselschichtzulage_pro_stunde'] = zeilendaten[1].wechselschichtzulage
                        inhalt = "{:,.2f}€".format(zeilendaten[1].wechselschichtzulage_schicht)
                    else:
                        inhalt = ''
                    width = 8

                if spaltennummer < 10:
                    if zeilendaten[1] != 'empty':
                        if text != '':
                            if command == 'kill':
                                zelle = tk.Button(tabelle, text=text, command=lambda: kill_schicht(key_string))
                            elif command == 'edit':
                                zelle = tk.Button(tabelle, text=text)
                            zelle.image = tk.PhotoImage(file=image, width=16, height=16)
                            zelle.config(image=zelle.image, width=16, height=16)
                            zelle.grid(row=zaehler, column=spaltennummer)
                            zeile.append(zelle)

                elif spaltennummer >= 10:
                    zelle = tk.Entry(tabelle, width=width)
                    zelle.grid(row=zaehler, column=spaltennummer)
                    zelle.delete(0, "end")
                    zelle.insert(0, inhalt)
                    zelle.config(state='readonly')
                    zeile.append(zelle)

            meine_tabelle.append(zeile)

    for widget in fenster.winfo_children():
        widget.destroy()
    nav = tk.Frame(fenster)
    tabelle = tk.Frame(fenster)
    seitenleiste = tk.Frame(fenster)

    if assistent.assistent_is_loaded == 1:
        hallo = tk.Label(fenster, text="Hallo " + str(assistent))
        hallo.grid(row=0, column=0)

    def erstelle_seitenleiste():
        for slwidget in seitenleiste.winfo_children():
            slwidget.destroy()

        # Header
        header = tk.Label(seitenleiste, text="Bezeichung", borderwidth=2, relief="groove")
        header.grid(row=0, column=0)
        header = tk.Label(seitenleiste, text="Stunden", borderwidth=2, relief="groove")
        header.grid(row=0, column=1)
        header = tk.Label(seitenleiste, text="pro Stunde", borderwidth=2, relief="groove")
        header.grid(row=0, column=2)
        header = tk.Label(seitenleiste, text="Gesamt", borderwidth=2, relief="groove")
        header.grid(row=0, column=3)

        bruttolohn = 0

        arbeitsstunden = tk.Label(seitenleiste, text="Arbeitsstunden:", borderwidth=2, relief="groove")
        arbeitsstunden.grid(row=1, column=0)
        arbeitsstunden_value = tk.Label(seitenleiste,
                                        text="{:,.2f}".format(round(tabelle.summen['arbeitsstunden'], 2)),
                                        borderwidth=2, relief="groove")
        arbeitsstunden_value.grid(row=1, column=1)
        # TODO wechsel der Erfahrungsstufe beachten

        stundenlohn_value = tk.Label(seitenleiste,
                                     text="{:,.2f}€".format(round(tabelle.summen['grundlohn_pro_stunde'], 2)),
                                     borderwidth=2,
                                     relief="groove")
        stundenlohn_value.grid(row=1, column=2)

        bruttolohn += tabelle.summen['grundlohn']
        arbeitsstunden_value = tk.Label(seitenleiste,
                                        text="{:,.2f}€".format(round(tabelle.summen['grundlohn'], 2)),
                                        borderwidth=2, relief="groove")
        arbeitsstunden_value.grid(row=1, column=3)

        nachtstunden = tk.Label(seitenleiste, text="Nachtstunden:", borderwidth=2, relief="groove")
        nachtstunden.grid(row=2, column=0)
        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}".format(round(tabelle.summen['nachtstunden'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=1)

        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}€".format(round(tabelle.summen['nachtzuschlag_pro_stunde'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=2)

        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}€".format(round(tabelle.summen['nachtzuschlag'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=3)
        bruttolohn += tabelle.summen['nachtzuschlag']
        rowcounter = 2
        for zuschlagsgrund in tabelle.summen['zuschlaege']:
            if tabelle.summen['zuschlaege'][zuschlagsgrund]['stunden_gesamt'] > 0:
                zuschl = tabelle.summen['zuschlaege'][zuschlagsgrund]
                rowcounter += 1
                nachtstunden = tk.Label(seitenleiste, text="Zuschlag " + zuschlagsgrund, borderwidth=2, relief="groove")
                nachtstunden.grid(row=rowcounter, column=0)

                nachtstunden_value = tk.Label(seitenleiste,
                                              text="{:,.2f}".format(round(zuschl['stunden_gesamt'], 2)),
                                              borderwidth=2,
                                              relief="groove")
                nachtstunden_value.grid(row=rowcounter, column=1)

                nachtstunden_value = tk.Label(seitenleiste,
                                              text="{:,.2f}€".format(round(zuschl['zuschlag_pro_stunde'], 2)),
                                              borderwidth=2,
                                              relief="groove")
                nachtstunden_value.grid(row=rowcounter, column=2)

                nachtstunden_value = tk.Label(seitenleiste,
                                              text="{:,.2f}€".format(round(zuschl['zuschlaege_gesamt'], 2)),
                                              borderwidth=2,
                                              relief="groove")
                nachtstunden_value.grid(row=rowcounter, column=3)
                bruttolohn += zuschl['zuschlaege_gesamt']

        rowcounter += 1
        nachtstunden = tk.Label(seitenleiste, text="Wechselschichtzulage:", borderwidth=2, relief="groove")
        nachtstunden.grid(row=2, column=0)
        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}".format(round(tabelle.summen['arbeitsstunden'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=1)

        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}€".format(
                                          round(tabelle.summen['wechselschichtzulage_pro_stunde'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=2)

        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}€".format(round(tabelle.summen['wechselschichtzulage'], 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=2, column=3)
        bruttolohn += tabelle.summen['nachtzuschlag']

        rowcounter += 1
        nachtstunden = tk.Label(seitenleiste, text="Summe = Bruttolohn", borderwidth=2, relief="groove")
        nachtstunden.grid(row=rowcounter, column=0)

        nachtstunden_value = tk.Label(seitenleiste,
                                      text="{:,.2f}€".format(round(bruttolohn, 2)),
                                      borderwidth=2,
                                      relief="groove")
        nachtstunden_value.grid(row=rowcounter, column=3)

        # TODO besseren Paltz für Kappung finden
        if tabelle.summen['wechselschichtzulage'] >= 105:
            tabelle.summen['wechselschichtzulage'] = 105
            rowcounter += 1
            nachtstunden = tk.Label(seitenleiste,
                                    text="Übersteigt die Wechselschitzulage 105€ wird auf diesen Betrag gekappt",
                                    borderwidth=2, relief="groove", columnspan=3)
            nachtstunden.grid(row=2, column=0)
            nachtstunden_value = tk.Label(seitenleiste,
                                          text="{:,.2f}".format(105),
                                          borderwidth=2,
                                          relief="groove")
            nachtstunden_value.grid(row=2, column=3)
        bruttolohn += tabelle.summen['wechselschichtzulage']

    erstelle_navigation()
    nav.grid(row=1, column=0)
    erstelle_tabelle()
    tabelle.grid(row=2, column=0)
    erstelle_seitenleiste()
    seitenleiste.grid(row=1, column=1, rowspan=2)

    # 2 Frames Für Navigation und Tabelle


assistent = AS()
lohntabelle = LohnTabelle()
root = tk.Tk()
root.geometry('1000x1000')
root.title("Dein Assistentenlohn")

fenster = tk.Frame(root)
fenster.pack()
info_text = tk.Label(fenster, text="Bitte erstelle oder öffne eine Assistenten-Datei")
info_text.grid(row=0, column=0, columnspan=2)
button_oeffnen = tk.Button(fenster, text="Gespeicherten Assistenten laden", command=alles_laden)
button_oeffnen.grid(row=1, column=0)
button_neu = tk.Button(fenster, text="Neuen Assistenten anlegen", command=neuer_as)
button_neu.grid(row=1, column=1)

fenster.mainloop()
