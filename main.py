import datetime
import pickle

import tkinter as tk
from tkcalendar import Calendar
import tkinter.filedialog as filedialog
import tkinter.messagebox as mb


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


class Adresse:
    def __init__(self, kuerzel, strasse, hnr, plz, stadt):
        self.strasse = strasse
        self.hnr = hnr
        self.plz = plz
        self.stadt = stadt
        self.kuerzel = kuerzel

    def __str__(self):
        return self.kuerzel


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
        self.home = Adresse('home', '', '', '', '')
        self.einstellungsdatum = einstellungsdatum
        self.__class__.count += 1
        self.festeSchichten = []
        self.urlaub = []
        self.au = []
        self.eb_liste = []
        self.pfk_liste = []
        self.letzte_eingetragene_schicht = {"beginn": datetime.datetime.now(),
                                            "ende": datetime.datetime.now(),
                                            "asn": "Neuer ASN"}

        self.adressen = []
        # TODO in Config auslagern
        self.adressen.append(Adresse(kuerzel="Hauptstelle - Urbanstraße", strasse="Urbanstr.",
                                     hnr="100", plz="10967", stadt="Berlin"))
        self.adressen.append(Adresse(kuerzel="Südbüro - Mehringhof", strasse="Gneisenaustr.",
                                     hnr="2a", plz="10961", stadt="Berlin"))
        self.adressen.append(Adresse(kuerzel="NO-W-BR-Büro", strasse="Wilhelm-Kabus-Str.",
                                     hnr="27-30", plz="10829", stadt="Berlin"))

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

    def get_adresse_by_kuerzel(self, kuerzel):
        for adresse in self.adressen:
            if adresse.kuerzel == kuerzel:
                return adresse
        return []

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

    def get_eb_by_string(self, string):
        data = string.split()
        for eb in self.eb_liste:
            if eb.vorname == data[0]:
                if len(data) > 1:
                    if data[1] == eb.name:
                        return eb
                else:
                    return eb

    # TODO optimieren
    def get_pfk_by_string(self, string):
        data = string.split()
        for pfk in self.pfk_liste:
            if pfk.vorname == data[0]:
                if len(data) > 1:
                    if pfk.name == data[1]:
                        return pfk
                return pfk


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
        self.schicht_templates = []
        self.eb = EB('', '', '')
        self.pfk = PFK('', '', '')
        self.adressen = []

    def get_kuerzel(self):
        return self.kuerzel

    def get_adresse_by_kuerzel(self, kuerzel):
        for adresse in self.adressen:
            if adresse.kuerzel == kuerzel:
                return adresse
        return []


class EB(Person):
    def __init__(self, name, vorname, email):
        self.name = name
        self.vorname = vorname
        self.email = email

    def __str__(self):
        return self.vorname + ' ' + self.name


class PFK(Person):
    def __init__(self, name, vorname, email):
        self.name = name
        self.vorname = vorname
        self.email = email

    def __str__(self):
        return self.vorname + ' ' + self.name


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
        self.orgazulage = lohntabelle.get_zuschlag('Orga', beginn)
        self.orgazulage_schicht = self.orgazulage * self.stundenzahl
        self.nachtstunden = self.berechne_anzahl_nachtstunden()
        self.nachtzuschlag = lohntabelle.get_zuschlag('Nacht', beginn)
        self.nachtzuschlag_schicht = self.nachtstunden * self.nachtzuschlag
        self.zuschlaege = self.berechne_sa_so_weisil_feiertagszuschlaege()
        self.ist_kurzfristig = 0
        self.ist_ausfallgeld = 0
        self.ist_assistententreffen = 0
        self.ist_pcg = 0
        self.ist_schulung = 0
        self.beginn_andere_adresse = ''
        self.ende_andere_adresse = ''

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
                    feiertagsstunden = get_duration(dreizehn_uhr, self.ende, 'hours')
                else:  # self.ende > einundzwanzig_uhr:
                    feiertagsstunden = 8  # 21 - 13
            elif dreizehn_uhr <= self.beginn < einundzwanzig_uhr:
                if self.ende < einundzwanzig_uhr:
                    feiertagsstunden = self.berechne_stundenzahl()
                elif self.ende > einundzwanzig_uhr:
                    feiertagsstunden = get_duration(self.beginn, einundzwanzig_uhr, 'hours')
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
                zuschlagsgrund = '24/31.12'
            if datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                    datetime.date(self.beginn.year, 12, 31):
                zuschlagsgrund = '24/31.12'

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
                    feiertagsstunden_steuerpflichtig = get_duration(self.beginn, vierzehn_uhr, 'hours')
                    feiertagsstunden_steuerfrei = get_duration(vierzehn_uhr, self.ende, 'hours')

            zuschlag = lohntabelle.get_zuschlag(zuschlag='24/31.12', schichtdatum=self.beginn)
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
            tmp = tmp - 31
        tmp = int(round(tmp))
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
                           'Feiertag': 22.80, 'Wechselschicht': 0.63, 'Orga': 0.20, '24/31.12': 5.72,
                           'Überstunde': 4.48}
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


class Menuleiste(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        # Menü Datei und Help erstellen
        datei_menu = tk.Menu(self, tearoff=0)
        datei_menu.add_command(label="Neue Assistenten-Datei", command=lambda: NeuerAS(root))
        datei_menu.add_command(label="Assistenten-Datei laden", command=alles_laden)
        datei_menu.add_command(label="Assistenten-Datei speichern", command=alles_speichern)
        # dateimenu.add_command(label="Assistenten-Datei speichern unter")
        datei_menu.add_separator()  # Fügt eine Trennlinie hinzu
        datei_menu.add_command(label="Exit", command=root.fenster.quit)

        eintragen_menu = tk.Menu(self, tearoff=0)
        eintragen_menu.add_command(label="Schicht eintragen", command=lambda: FensterNeueSchicht(root))
        eintragen_menu.add_command(label="Urlaub eintragen", command=lambda: NeuerUrlaub(root))
        eintragen_menu.add_command(label="AU/krank eintragen", command=lambda: NeueAU(root))

        bearbeiten_menu = tk.Menu(self, tearoff=0)
        bearbeiten_menu.add_command(label="ASN bearbeiten", command=lambda: FensterEditAsn(root))
        bearbeiten_menu.add_command(label="Assistent bearbeiten", command=lambda: NeuerAS(root, edit=1))

        taxes_menu = tk.Menu(self, tearoff=0)
        taxes_menu.add_command(label="Berechne Abwesenheit für Verpflegungsmehraufwand")
        taxes_menu.add_command(label="Berechne Fahrtzeiten für Reisekosten")

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="Info!", command=action_get_info_dialog)

        self.add_cascade(label="Datei", menu=datei_menu)
        self.add_cascade(label="Eintragen", menu=eintragen_menu)
        self.add_cascade(label="Bearbeiten", menu=bearbeiten_menu)
        self.add_cascade(label="Einkommenssteuer", menu=taxes_menu)
        self.add_cascade(label="Help", menu=help_menu)


class NeuerAS(tk.Toplevel):
    def __init__(self, parent, edit=0):
        super().__init__(parent)
        self.parent = parent
        headline = tk.Label(self, text="Wer bist du denn eigentlich?")
        vorname_label = tk.Label(self, text="Vorname")
        self.vorname_input = tk.Entry(self, bd=5, width=40)
        nachname_label = tk.Label(self, text="Nachname")
        self.nachname_input = tk.Entry(self, bd=5, width=40)
        email_label = tk.Label(self, text="Email")
        self.email_input = tk.Entry(self, bd=5, width=40)
        strasse_label = tk.Label(self, text="Straße/Hausnummer")
        self.strasse_input = tk.Entry(self, bd=5, width=29)
        self.hausnummer_input = tk.Entry(self, bd=5, width=9)
        plz_label = tk.Label(self, text="Postleitzahl")
        self.plz_input = tk.Entry(self, bd=5, width=40)
        stadt_label = tk.Label(self, text="Stadt")
        self.stadt_input = tk.Entry(self, bd=5, width=40)
        einstellungsdatum_label = tk.Label(self, text="Seit wann bei ad? (tt.mm.JJJJ)")
        self.einstellungsdatum_input = Calendar(self)
        self.save_button = tk.Button(self, text="Daten speichern", command=self.action_save_neuer_as)
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)

        if edit:
            self.vorname_input.insert(0, assistent.vorname)
            self.nachname_input.insert(0, assistent.name)
            self.email_input.insert(0, assistent.email)
            self.strasse_input.insert(0, assistent.home.strasse)
            self.hausnummer_input.insert(0, assistent.home.hnr)
            self.plz_input.insert(0, assistent.home.plz)
            self.stadt_input.insert(0, assistent.home.stadt)

        # ins Fenster packen
        headline.grid(row=0, column=0, columnspan=3)
        vorname_label.grid(row=1, column=0)
        self.vorname_input.grid(row=1, column=1, columnspan=2)
        nachname_label.grid(row=2, column=0)
        self.nachname_input.grid(row=2, column=1, columnspan=2)
        email_label.grid(row=3, column=0)
        self.email_input.grid(row=3, column=1, columnspan=2)
        strasse_label.grid(row=4, column=0)
        self.strasse_input.grid(row=4, column=1)
        self.hausnummer_input.grid(row=4, column=2)
        plz_label.grid(row=5, column=0)
        self.plz_input.grid(row=5, column=1, columnspan=2)
        stadt_label.grid(row=6, column=0)
        self.stadt_input.grid(row=6, column=1, columnspan=2)

        # TODO Text nach oben
        einstellungsdatum_label.grid(row=7, column=0)
        self.einstellungsdatum_input.grid(row=7, column=1)
        self.exit_button.grid(row=8, column=0)
        self.save_button.grid(row=8, column=1)

    def action_save_neuer_as(self):
        global assistent
        einstellungsdatum_date_obj = datetime.datetime.strptime(self.einstellungsdatum_input.get_date(),
                                                                '%m/%d/%y')
        assistent = AS(self.nachname_input.get(), self.vorname_input.get(),
                       self.email_input.get(), einstellungsdatum_date_obj)
        assistent.home = Adresse(kuerzel='home',
                                 strasse=self.strasse_input.get(),
                                 hnr=self.hausnummer_input.get(),
                                 plz=self.plz_input.get(),
                                 stadt=self.stadt_input.get())
        assistent.__class__.assistent_is_loaded = 1
        alles_speichern(neu=1)
        self.destroy()


class FensterEditAsn(tk.Toplevel):
    class AsnAuswahllisteFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.asn_options = list(assistent.get_all_asn().keys())
            self.selected_asn = tk.StringVar()
            self.asn_options.insert(0, "Neuer ASN")
            self.selected_asn.set("Neuer ASN")

            for kuerzel in self.asn_options:
                button = tk.Radiobutton(self, text=kuerzel, padx=20,
                                        variable=self.selected_asn, value=kuerzel,
                                        command=self.choose_asn)
                button.pack()

        def choose_asn(self):
            kuerzelAusgewaehlt = self.selected_asn.get()
            self.parent.editframe.destroy()
            self.parent.editframe = self.parent.AsnEditFrame(self.parent, kuerzelAusgewaehlt)
            self.parent.editframe.grid(row=0, column=1)

    class AsnEditFrame(tk.Frame):
        class FesteSchichtForm(tk.Frame):
            class FesteSchichtTabelle(tk.Frame):

                def __init__(self, parent, asn):
                    global assistent
                    super().__init__(parent)
                    self.asn = asn
                    self.draw()

                def draw(self):
                    for child in self.winfo_children():
                        child.destroy()
                    rowcounter = 0
                    eintrag = tk.Label(self, text='Deine festen Schichten\nin diesem Einsatz')
                    eintrag.grid(row=rowcounter, column=0)
                    rowcounter += 1
                    for feste_schicht in assistent.festeSchichten:
                        if feste_schicht['asn'] == self.asn.kuerzel:
                            text = feste_schicht['wochentag'] + ', '
                            text += feste_schicht['start'].strftime("%H:%M") + ' - '
                            text += feste_schicht['ende'].strftime("%H:%M")
                            eintrag = tk.Label(self, text=text)
                            eintrag.grid(row=rowcounter, column=0)
                            rowcounter += 1

            def __init__(self, parent, asn):
                super().__init__(parent)
                self.asn = asn
                headline = tk.Label(self, text='Feste Schichten erstellen/bearbeiten')
                headline.grid(row=0, column=0, columnspan=3)
                jeden = tk.Label(self, text="Jeden")
                jeden.grid(row=1, column=0)
                wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
                              'Auswählen']
                self.gewaehlter_tag = tk.StringVar()
                self.gewaehlter_tag.set(wochentage[7])
                form_wochentage_dropdown = tk.OptionMenu(self, self.gewaehlter_tag, *wochentage)
                form_wochentage_dropdown.grid(row=1, column=1)
                von = tk.Label(self, text="Von")
                von.grid(row=2, column=0)
                self.startzeit_input = TimePicker(self)
                self.startzeit_input.grid(row=2, column=1)
                bis = tk.Label(self, text="bis")
                bis.grid(row=3, column=0)
                self.endzeit_input = TimePicker(self)
                self.endzeit_input.grid(row=3, column=1)
                self.schichtliste = self.FesteSchichtTabelle(self, asn)
                self.schichtliste.grid(row=1, column=3, rowspan=3)
                submit_button = tk.Button(self, text='feste Schicht hinzufügen',
                                          command=self.save_feste_schicht)
                submit_button.grid(row=4, column=1, columnspan=2)

            def save_feste_schicht(self):
                global assistent
                if self.gewaehlter_tag.get() != 'Auswählen':
                    wochentag = self.gewaehlter_tag.get()
                    startzeit_stunde = int(self.startzeit_input.hourstr.get())
                    startzeit_minute = int(self.startzeit_input.minstr.get())
                    endzeit_stunde = int(self.endzeit_input.hourstr.get())
                    endzeit_minute = int(self.endzeit_input.minstr.get())
                    s_feste_schicht = {'asn': self.asn.kuerzel,
                                       'wochentag': wochentag,
                                       'start': datetime.time(startzeit_stunde, startzeit_minute, 0),
                                       'ende': datetime.time(endzeit_stunde, endzeit_minute, 0)}
                    assistent.festeSchichten.append(s_feste_schicht)
                    self.schichtliste.draw()
                    alles_speichern()

        class SchichtTemplateForm(tk.Frame):
            class TemplateTabelle(tk.Frame):

                def __init__(self, parent, asn):
                    global assistent
                    super().__init__(parent)
                    self.asn = asn
                    self.draw()

                def draw(self):
                    for child in self.winfo_children():
                        child.destroy()
                    rowcounter = 0
                    eintrag = tk.Label(self, text='Deine Vorlagen\nfür diesem Einsatz')
                    eintrag.grid(row=rowcounter, column=0)
                    rowcounter += 1
                    for template in self.asn.schicht_templates:
                        text = template['bezeichner'] + ': '
                        text += template['start'].strftime("%H:%M") + ' - '
                        text += template['ende'].strftime("%H:%M")
                        eintrag = tk.Label(self, text=text)
                        eintrag.grid(row=rowcounter, column=0)
                        rowcounter += 1

            def __init__(self, parent, asn):
                self.asn = asn
                super().__init__(parent)
                headline = tk.Label(self, text='Schichtvorlagen erstellen/bearbeiten')
                headline.grid(row=0, column=0, columnspan=2)
                bezeichner = tk.Label(self, text="Bezeichner (z.B. \"Frühschicht\")")
                bezeichner.grid(row=1, column=0)
                self.bezeichner = tk.Entry(self)
                self.bezeichner.grid(row=1, column=1)
                von = tk.Label(self, text="Von")
                von.grid(row=2, column=0)
                self.startzeit_input = TimePicker(self)
                self.startzeit_input.grid(row=2, column=1)
                bis = tk.Label(self, text="bis")
                bis.grid(row=3, column=0)
                self.endzeit_input = TimePicker(self)
                self.endzeit_input.grid(row=3, column=1)
                self.templateliste = self.TemplateTabelle(self, asn=asn)
                self.templateliste.grid(row=1, column=3, rowspan=3)

                submit_button = tk.Button(self, text='Schichtvorlage hinzufügen',
                                          command=self.save_schicht_template)
                submit_button.grid(row=4, column=1, columnspan=2)

            def save_schicht_template(self):
                bezeichner = self.bezeichner.get()
                startzeit_stunde = int(self.startzeit_input.hourstr.get())
                startzeit_minute = int(self.startzeit_input.minstr.get())
                endzeit_stunde = int(self.endzeit_input.hourstr.get())
                endzeit_minute = int(self.endzeit_input.minstr.get())
                s_feste_schicht = {'bezeichner': bezeichner,
                                   'start': datetime.time(startzeit_stunde, startzeit_minute, 0),
                                   'ende': datetime.time(endzeit_stunde, endzeit_minute, 0)}
                self.asn.schicht_templates.append(s_feste_schicht)
                self.templateliste.draw()
                # zeichne_feste_schichten_form(self)

        class AsnStammdatenForm(tk.Frame):
            def __init__(self, parent, asn):
                self.asn = asn
                super().__init__(parent)
                kuerzel_label = tk.Label(self, text="Kürzel")
                self.kuerzel_input = tk.Entry(self, bd=5, width=40)
                vorname_label = tk.Label(self, text="Vorname")
                self.vorname_input = tk.Entry(self, bd=5, width=40)
                nachname_label = tk.Label(self, text="Nachname")
                self.nachname_input = tk.Entry(self, bd=5, width=40)
                strasse_label = tk.Label(self, text="Straße/Hausnummer")
                self.strasse_input = tk.Entry(self, bd=5, width=29)
                self.hausnummer_input = tk.Entry(self, bd=5, width=9)
                plz_label = tk.Label(self, text="Postleitzahl")
                self.plz_input = tk.Entry(self, bd=5, width=40)
                stadt_label = tk.Label(self, text="Stadt")
                self.stadt_input = tk.Entry(self, bd=5, width=40)
                buero_label = tk.Label(self, text="Zuständiges Einsatzbüro")
                # TODO in Klassen überführen
                option_list = ['Bitte auswählen', 'Nordost', 'West', 'Süd']
                self.selected_buero = tk.StringVar()
                self.selected_buero.set(option_list[0])
                self.buero_dropdown = tk.OptionMenu(self, self.selected_buero, *option_list)
                if self.asn != 'Neuer ASN':
                    self.kuerzel_input.insert(0, self.asn.kuerzel)
                    if self.asn.kuerzel != '':
                        self.kuerzel_input.config(state='disabled')
                    self.vorname_input.insert(0, self.asn.vorname)
                    self.nachname_input.insert(0, self.asn.name)
                    self.strasse_input.insert(0, self.asn.strasse)
                    self.hausnummer_input.insert(0, self.asn.hausnummer)
                    self.plz_input.insert(0, self.asn.plz)
                    self.stadt_input.insert(0, self.asn.stadt)

                # positionieren
                kuerzel_label.grid(row=0, column=0)
                self.kuerzel_input.grid(row=0, column=1, columnspan=2)
                vorname_label.grid(row=1, column=0)
                self.vorname_input.grid(row=1, column=1, columnspan=2)
                nachname_label.grid(row=2, column=0)
                self.nachname_input.grid(row=2, column=1, columnspan=2)
                strasse_label.grid(row=3, column=0)
                self.strasse_input.grid(row=3, column=1)
                self.hausnummer_input.grid(row=3, column=2)
                plz_label.grid(row=4, column=0)
                self.plz_input.grid(row=4, column=1, columnspan=2)
                stadt_label.grid(row=5, column=0)
                self.stadt_input.grid(row=5, column=1, columnspan=2)
                buero_label.grid(row=6, column=0)
                self.buero_dropdown.grid(row=6, column=1)

            def show(self):
                self.grid()

            def hide(self):
                self.grid_remove()

            def save_stammdaten(self):
                # Stammdaten speichern
                vname = self.vorname_input.get()
                name = self.nachname_input.get()
                strasse = self.strasse_input.get()
                hnr = self.hausnummer_input.get()
                plz = self.plz_input.get()
                stadt = self.stadt_input.get()
                neues_kuerzel = self.kuerzel_input.get()

                if self.asn == 'Neuer ASN':
                    asn = ASN(name, vname, neues_kuerzel, strasse, hnr, plz, stadt)
                else:
                    asn = self.asn
                    asn.vorname = vname
                    asn.name = name
                    asn.strasse = strasse
                    asn.hausnummer = hnr
                    asn.stadt = stadt
                    asn.plz = plz
                    asn.kuerzel = neues_kuerzel

                asn.buero = self.selected_buero.get()
                return asn

        class EbPfkEditForm(tk.Frame):
            def __init__(self, parent, asn, eb_oder_pfk):
                self.asn = asn
                super().__init__(parent)

                first, text, liste, select_what = '', '', [], []

                self.selected = tk.StringVar()
                if eb_oder_pfk == 'eb':
                    text = "Einsatzbegleitung"
                    liste = assistent.eb_liste
                    first = "Neue EB"
                    select_what = asn.eb
                    if self.asn.eb:
                        if asn.eb.name == '' and asn.eb.vorname == '':
                            self.selected.set(first)
                        else:
                            self.selected.set(select_what)
                    else:
                        self.selected.set(first)
                elif eb_oder_pfk == 'pfk':
                    text = "Pflegefachkraft"
                    liste = assistent.pfk_liste
                    first = "Neue PFK"
                    select_what = asn.pfk
                    if self.asn.pfk:
                        if self.asn.pfk.name == '' and self.asn.pfk.vorname == '':
                            self.selected.set(first)
                        else:
                            self.selected.set(select_what)
                    else:
                        self.selected.set(first)
                headline = tk.Label(self, text=text)
                option_list = [first, *liste]

                self.eb_dropdown = tk.OptionMenu(self, self.selected, *option_list, command=self.change_person)

                vorname_label = tk.Label(self, text="Vorname")
                self.vorname_input = tk.Entry(self, bd=5, width=40)
                nachname_label = tk.Label(self, text="Nachname")
                self.nachname_input = tk.Entry(self, bd=5, width=40)
                email_label = tk.Label(self, text="Email")
                self.email_input = tk.Entry(self, bd=5, width=40)

                if select_what:
                    self.vorname_input.insert(0, select_what.vorname)
                    self.nachname_input.insert(0, select_what.name)
                    self.email_input.insert(0, select_what.email)

                headline.grid(row=0, column=0)
                self.eb_dropdown.grid(row=0, column=1)
                vorname_label.grid(row=1, column=0)
                self.vorname_input.grid(row=1, column=1)
                nachname_label.grid(row=2, column=0)
                self.nachname_input.grid(row=2, column=1)
                email_label.grid(row=3, column=0)
                self.email_input.grid(row=3, column=1)

            def change_person(self, person):
                self.vorname_input.delete(0, 'end')
                self.nachname_input.delete(0, 'end')
                self.email_input.delete(0, 'end')
                if person != 'Neue EB' and person != 'Neue PFK':
                    self.vorname_input.insert(0, person.vorname)
                    self.nachname_input.insert(0, person.name)
                    self.email_input.insert(0, person.email)

            def save_person(self, eb_oder_pfk='eb'):
                if eb_oder_pfk == 'eb':
                    person = self.asn.eb
                else:
                    person = self.asn.pfk

                if self.nachname_input.get() != '' \
                        or self.vorname_input.get() != '' \
                        or self.email_input.get() != '':

                    if eb_oder_pfk == 'eb':
                        abgleich = assistent.get_eb_by_string(self.selected.get())
                    else:
                        abgleich = assistent.get_pfk_by_string(self.selected.get())

                    if self.selected.get() == "Neue EB" or self.selected.get == "Neue PFK":
                        person = EB(name=self.nachname_input.get(),
                                    vorname=self.vorname_input.get(),
                                    email=self.email_input.get())
                    elif abgleich == person:
                        # aktuelle person bearbeiten

                        person.name = self.nachname_input.get()
                        person.vorname = self.vorname_input.get()
                        person.email = self.email_input.get()
                    else:
                        person = assistent.get_eb_by_string(self.selected.get())

                    if eb_oder_pfk == 'eb':
                        self.asn.eb = person
                    else:
                        self.asn.pfk = person
                    if person not in assistent.eb_liste and eb_oder_pfk == 'eb':
                        assistent.eb_liste.append(person)
                    elif person not in assistent.pfk_liste and eb_oder_pfk == 'pfk':
                        assistent.pfk_liste.append(person)

        def __init__(self, parent, kuerzel):

            global assistent
            super().__init__(parent)
            self.parent = parent
            if kuerzel == 'Neuer ASN':
                self.asn = ASN('', '', '', '', '', '', 'Berlin')
            else:
                self.asn = assistent.get_asn_by_kuerzel(kuerzel)

            self.stammdatenframe = self.AsnStammdatenForm(self, self.asn)
            self.stammdatenframe.grid(row=0, column=0, rowspan=2)
            self.eb_frame = self.EbPfkEditForm(self, self.asn, 'eb')
            self.eb_frame.grid(row=0, column=1)

            # todo fix PFK
            # self.pfk_frame = self.EbPfkEditForm(self, self.asn, 'pfk')
            # self.pfk_frame.grid(row=1, column=1)

            self.feste_schichten_frame = self.FesteSchichtForm(self, self.asn)
            self.feste_schichten_frame.grid(row=2, column=0)
            self.schicht_templates_frame = self.SchichtTemplateForm(self, self.asn)
            self.schicht_templates_frame.grid(row=2, column=1)

            save_button = tk.Button(self, text="Daten speichern", command=lambda: self.save_asn_edit_form())
            exit_button = tk.Button(self, text="Fenster schließen",
                                    command=parent.destroy)
            save_button.grid(row=5, column=1)
            exit_button.grid(row=5, column=0)

        def save_asn_edit_form(self):
            global assistent
            asn = self.stammdatenframe.save_stammdaten()
            self.eb_frame.save_person(eb_oder_pfk='eb')
            # self.pfk_frame.save_person(eb_oder_pfk='pfk')
            assistent.asn[asn.kuerzel] = asn
            alles_speichern()
            self.parent.destroy()
            FensterEditAsn(root)

    def __init__(self, parent):
        global assistent
        super().__init__(parent)
        self.auswahlframe = self.AsnAuswahllisteFrame(self)
        self.auswahlframe.grid(row=0, column=0)
        self.editframe = self.AsnEditFrame(self, "Neuer ASN")
        self.editframe.grid(row=0, column=1)


class FensterNeueSchicht(tk.Toplevel):
    class AsnFrame(tk.Frame):
        class SchichtTemplates(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)
                self.parent = parent

                self.kuerzel = parent.parent.asn_frame.selected_asn.get()
                if self.kuerzel != 'Bitte auswählen':
                    # kuerzel = parent.parent.asn_frame.selected_asn.get()
                    self.asn = assistent.get_asn_by_kuerzel(self.kuerzel)
                    self.templates = self.asn.schicht_templates
                    self.selected_template = tk.IntVar()
                    self.selected_template.set(0)
                    self.change_template()
                    self.draw_templates()

            def draw_templates(self):
                self.kuerzel = self.parent.parent.asn_frame.selected_asn.get()
                if self.kuerzel != 'Bitte auswählen':
                    # kuerzel = parent.parent.asn_frame.selected_asn.get()
                    asn = assistent.get_asn_by_kuerzel(self.kuerzel)
                    self.templates = asn.schicht_templates
                    self.selected_template = tk.IntVar()
                    self.selected_template.set(0)
                    self.change_template()
                    col = 0
                    row = 0
                    counter = 0
                    for template in self.templates:
                        text = template['bezeichner'] + " von " + template["start"].strftime('%H:%M') \
                               + " bis " + template["ende"].strftime('%H:%M')
                        button = tk.Radiobutton(self, text=text,
                                                variable=self.selected_template, value=counter,
                                                command=lambda: self.change_template())
                        button.grid(row=row, column=col)
                        counter += 1
                        col += 1
                        if col == 4:
                            col = 0
                            row += 1

            def change_template(self):
                if self.kuerzel != "Bitte auswählen" and self.kuerzel != "Neuer Assistent":

                    asn = assistent.get_asn_by_kuerzel(self.kuerzel)
                    if asn.schicht_templates:
                        template_index = self.selected_template.get()
                        template = asn.schicht_templates[template_index]
                        start = template["start"]
                        ende = template["ende"]
                        frame = self.parent.parent.schicht_calendar_frame
                        frame.startzeit_input.hourstr.set(start.strftime("%H"))
                        frame.startzeit_input.minstr.set(start.strftime("%M"))
                        frame.endzeit_input.hourstr.set(ende.strftime("%H"))
                        frame.endzeit_input.minstr.set(ende.strftime("%M"))
                        if ende < start:
                            frame.tag_nacht_reise_var.set(2)
                        else:
                            frame.tag_nacht_reise_var.set(1)

            def show(self):
                for child in self.winfo_children():
                    child.destroy()
                self.draw_templates()
                self.grid()

            def hide(self):
                self.grid_remove()

        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.asn_label = tk.Label(self, text="Assistenznehmer")
            # grundsätzliche Optionen für Dropdown
            option_list = ["Bitte auswählen", "Neuer ASN", *assistent.get_all_asn()]
            self.selected_asn = tk.StringVar()
            self.selected_asn.set(option_list[0])
            self.asn_dropdown = tk.OptionMenu(self, self.selected_asn, *option_list,
                                              command=self.change_asn)
            # self.neuer_asn = self.NeuerAsnInSchicht(self)
            self.neuer_asn = FensterEditAsn.AsnEditFrame.AsnStammdatenForm(self, "Neuer ASN")

            # positionieren
            self.asn_label.grid(row=1, column=0)
            self.asn_dropdown.grid(row=1, column=1)
            self.neuer_asn.grid(row=2, column=0)
            self.neuer_asn.hide()

        def change_asn(self, selected_asn):

            if selected_asn == "Neuer ASN":
                self.neuer_asn.show()
                self.parent.schicht_calendar_frame.templates.hide()
                self.parent.save_button.grid()
                self.parent.saveandnew_button.grid()
            elif selected_asn == "Bitte auswählen":
                self.neuer_asn.hide()
                self.parent.schicht_calendar_frame.templates.hide()
                self.parent.save_button.grid_remove()
                self.parent.saveandnew_button.grid_remove()
            else:
                self.parent.asn = assistent.get_asn_by_kuerzel(selected_asn)
                self.neuer_asn.hide()
                self.parent.schicht_calendar_frame.templates.show()
                self.parent.save_button.grid()
                self.parent.saveandnew_button.grid()

                # Schalter für Schicht ausser Haus

        def get_data(self):
            if self.selected_asn.get() == "Neuer ASN":
                asn = self.neuer_asn.save_stammdaten()
                assistent.asn_dazu(asn)
            else:
                asn = assistent.get_asn_by_kuerzel(self.selected_asn.get())
            return asn

    class SchichtCalendarFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.startdatum_label = tk.Label(self, text="Datum (Beginn) der Schicht")
            self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')

            self.startzeit_label = tk.Label(self, text="Startzeit")
            self.startzeit_input = TimePicker(self)
            self.startzeit_input.bind('<FocusOut>', self.nachtschicht_durch_uhrzeit)
            self.endzeit_label = tk.Label(self, text="Schichtende")
            self.endzeit_input = TimePicker(self)
            self.endzeit_input.bind('<FocusOut>', self.nachtschicht_durch_uhrzeit)

            self.enddatum_label = tk.Label(self, text="Datum Ende der Schicht")
            self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
            # TODO Vorauswahl konfigurieren lassen
            self.tag_nacht_reise_var = tk.IntVar()
            self.tag_nacht_reise_var.set(1)
            self.anderes_enddatum_label = tk.Label(self,
                                                   text="Tagschicht, Nachtschicht\noder mehrtägig?")
            self.anderes_enddatum_input_radio1 = \
                tk.Radiobutton(self, text="Tagschicht", padx=20,
                               variable=self.tag_nacht_reise_var, value=1,
                               command=lambda: self.tag_nacht_reise(1, self.enddatum_input,
                                                                    self.enddatum_label))
            self.anderes_enddatum_input_radio2 = \
                tk.Radiobutton(self, text="Nachtschicht\n(Ende der Schicht ist am Folgetag)", padx=20,
                               variable=self.tag_nacht_reise_var, value=2,
                               command=lambda: self.tag_nacht_reise(2, self.enddatum_input,
                                                                    self.enddatum_label))
            self.anderes_enddatum_input_radio3 = \
                tk.Radiobutton(self, text="Mehrtägig/Reisebegleitung", padx=20,
                               variable=self.tag_nacht_reise_var, value=3,
                               command=lambda: self.tag_nacht_reise(3, self.enddatum_input,
                                                                    self.enddatum_label))

            self.templates = parent.asn_frame.SchichtTemplates(self)

            # positionieren
            self.startdatum_label.grid(row=0, column=0, columnspan=2, rowspan=3)
            self.startdatum_input.grid(row=1, column=0, columnspan=2, rowspan=3)
            self.enddatum_label.grid(row=0, column=2, columnspan=2, rowspan=3)
            self.enddatum_input.grid(row=1, column=2, columnspan=2, rowspan=3)
            self.startzeit_label.grid(row=4, column=0)
            self.startzeit_input.grid(row=4, column=1)
            self.endzeit_label.grid(row=4, column=2)
            self.endzeit_input.grid(row=4, column=3)
            # TODO prüfen, wenn endzeit < startzeit nachtschicht im Radiobutton markieren
            self.anderes_enddatum_label.grid(row=0, column=2)
            # TODO zusätzliche Felder für Reisen

            self.anderes_enddatum_input_radio1.grid(row=1, column=4)
            self.anderes_enddatum_input_radio2.grid(row=2, column=4)
            self.anderes_enddatum_input_radio3.grid(row=3, column=4)

            self.templates.grid(row=5, column=0, columnspan=4)
            self.templates.hide()

            # TODO HACK besser machen? zwingt enddatum auf invisible
            self.tag_nacht_reise(1, self.enddatum_input,
                                 self.enddatum_label)

        def nachtschicht_durch_uhrzeit(self, event):
            start = datetime.time(hour=int(self.startzeit_input.hourstr.get()),
                                  minute=int(self.startzeit_input.minstr.get()))
            ende = datetime.time(hour=int(self.endzeit_input.hourstr.get()),
                                 minute=int(self.endzeit_input.minstr.get()))

            if ende < start:
                self.tag_nacht_reise_var.set(2)
            else:
                self.tag_nacht_reise_var.set(1)

        def tag_nacht_reise(self, value, label, button):
            if value == 3:
                label.grid()
                button.grid()
            elif value == 1 or value == 2:
                label.grid_remove()
                button.grid_remove()

        def get_data(self):
            startdatum = self.startdatum_input.get_date().split('/')
            beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                       int(self.startzeit_input.hourstr.get()),
                                       int(self.startzeit_input.minstr.get()))

            # ende der Schicht bestimmen. Fälle: Tagschicht, Nachtschicht, Reise
            # todo minstring darf nicht mehr als 59 sein. kann durch ungeduldiges tippen passieren entry validieren
            if self.tag_nacht_reise_var.get() == 1:  # Tagschicht
                ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))
            elif self.tag_nacht_reise_var.get() == 2:  # Nachtschicht
                ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]) + 1,
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))
            else:  # Reisebegleitung
                enddatum = self.enddatum_input.get_date().split('/')
                ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]),
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))

            return {'beginn': beginn, 'ende': ende}

    class SchichtAdditionalOptions(tk.Frame):
        class SchichtAusserHaus(tk.Frame):
            class AdressSelectOrInput(tk.Frame):
                def __init__(self, parent, master):
                    super().__init__(parent)
                    self.parent = parent
                    self.auswahl = []
                    self.auswahl.append('Keine abweichende Adresse')
                    self.auswahl.append('Neue Adresse eintragen')
                    standardadressen = assistent.adressen
                    for adresse in standardadressen:
                        self.auswahl.append(adresse)
                    self.asn = ''
                    kuerzel = master.get()
                    if kuerzel != "Neuer ASN" and kuerzel != "Bitte auswählen":
                        self.asn = assistent.get_asn_by_kuerzel(kuerzel)
                        if master.get() != assistent:
                            if self.asn.adressen:
                                self.auswahl.append(*master.adressen)
                    self.selected = tk.StringVar()
                    self.selected.set(self.auswahl[0])
                    dropdown = tk.OptionMenu(self, self.selected, *self.auswahl, command=self.change_dropdown)
                    dropdown.grid(row=0, column=0)

                    self.neue_adresse = tk.Frame(self)

                    self.kuerzel_label = tk.Label(self.neue_adresse, text="Bezeichner")
                    self.kuerzel_input = tk.Entry(self.neue_adresse, bd=5, width=40)
                    self.strasse_label = tk.Label(self.neue_adresse, text="Straße/Hausnummer")
                    self.strasse_input = tk.Entry(self.neue_adresse, bd=5, width=29)
                    self.hausnummer_input = tk.Entry(self.neue_adresse, bd=5, width=9)
                    self.plz_label = tk.Label(self.neue_adresse, text="Postleitzahl")
                    self.plz_input = tk.Entry(self.neue_adresse, bd=5, width=40)
                    self.stadt_label = tk.Label(self.neue_adresse, text="Stadt")
                    self.stadt_input = tk.Entry(self.neue_adresse, bd=5, width=40)

                    self.kuerzel_label.grid(row=0, column=0)
                    self.kuerzel_input.grid(row=0, column=1, columnspan=2)
                    self.strasse_label.grid(row=1, column=0)
                    self.strasse_input.grid(row=1, column=1)
                    self.hausnummer_input.grid(row=1, column=2)
                    self.plz_label.grid(row=2, column=0)
                    self.plz_input.grid(row=2, column=1, columnspan=2)
                    self.stadt_label.grid(row=3, column=0)
                    self.stadt_input.grid(row=3, column=1, columnspan=2)
                    self.neue_adresse.grid(row=1, column=0)
                    self.neue_adresse.grid_remove()

                def change_dropdown(self, selected):
                    if selected == 'Neue Adresse eintragen':
                        self.neue_adresse.grid()
                    else:
                        self.neue_adresse.grid_remove()

                def get_data(self):
                    if self.selected.get() == "Keine abweichende Adresse":
                        return []
                    elif self.selected.get() == "Neue Adresse eintragen":
                        adresse = Adresse(kuerzel=self.kuerzel_input.get(),
                                          strasse=self.strasse_input.get(),
                                          hnr=self.hausnummer_input.get(),
                                          plz=self.plz_input.get(),
                                          stadt=self.stadt_input.get())
                        self.parent.parent.parent.asn.adressen.append(adresse)
                        return adresse
                    else:
                        asn_adresse = self.parent.parent.parent.asn.get_adresse_by_kuerzel(self.selected.get())
                        if asn_adresse:
                            return asn_adresse
                        else:
                            as_adresse = assistent.get_adresse_by_kuerzel(self.selected.get())
                            return as_adresse

            def __init__(self, parent):
                super().__init__(parent)
                self.parent = parent
                master = self.parent.parent.asn_frame.selected_asn
                self.alternative_adresse_beginn_label = tk.Label(self,
                                                                 text="Beginn der Schicht außer Haus")
                self.alternative_adresse_beginn_input = self.AdressSelectOrInput(self, master)
                self.alternative_adresse_ende_label = tk.Label(self,
                                                               text="Ende der Schicht außer Haus")
                self.alternative_adresse_ende_input = self.AdressSelectOrInput(self, master)

                self.alternative_adresse_beginn_label.grid(row=0, column=0)
                self.alternative_adresse_beginn_input.grid(row=0, column=1)
                self.alternative_adresse_ende_label.grid(row=1, column=0)
                self.alternative_adresse_ende_input.grid(row=1, column=1)

            def get_data(self):
                return {'alt_adresse_beginn': self.alternative_adresse_beginn_input.get_data(),
                        'alt_adresse_ende': self.alternative_adresse_ende_input.get_data()}

        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent

            self.ist_at = tk.IntVar()
            self.ist_pcg = tk.IntVar()
            self.ist_rb = tk.IntVar()
            self.ist_afg = tk.IntVar()
            self.ist_at_button = tk.Checkbutton(self, text="AT", variable=self.ist_at, onvalue=1, offvalue=0)
            self.ist_pcg_button = tk.Checkbutton(self, text="PCG", variable=self.ist_pcg, onvalue=1, offvalue=0)
            self.ist_rb_button = tk.Checkbutton(self, text="Kurzfristig (RB/BSD)", variable=self.ist_rb, onvalue=1,
                                                offvalue=0)
            self.ist_afg_button = tk.Checkbutton(self, text="Ausfallgeld", variable=self.ist_afg, onvalue=1, offvalue=0)
            self.ausser_haus = self.SchichtAusserHaus(self)

            # positionieren
            self.ist_at_button.grid(row=0, column=0)
            self.ist_pcg_button.grid(row=0, column=1)
            self.ist_rb_button.grid(row=0, column=2)
            self.ist_afg_button.grid(row=0, column=3)

            self.ausser_haus.grid(row=1, column=0, columnspan=4)

        def get_data(self):
            return {"is_at": self.ist_at.get(),
                    "is_pcg": self.ist_pcg.get(),
                    "is_rb": self.ist_rb.get(),
                    "is_afg": self.ist_afg.get(),
                    "alternative adresse start": self.ausser_haus.get_data()["alt_adresse_beginn"],
                    "alternative adresse ende": self.ausser_haus.get_data()["alt_adresse_ende"]}

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.asn = ''
        self.asn_frame = self.AsnFrame(self)
        self.schicht_calendar_frame = self.SchichtCalendarFrame(self)
        self.schicht_add_options = self.SchichtAdditionalOptions(self)

        # positionieren
        self.asn_frame.grid(row=0, column=0, columnspan=3)
        self.schicht_calendar_frame.grid(row=1, column=0, columnspan=3)
        self.schicht_add_options.grid(row=2, column=0, columnspan=3)

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neue_schicht)
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu",
                                           command=lambda: self.action_save_neue_schicht(undneu=1))

        # wird erst bei "Neuer AS" zugeschaltet
        # self.templates.grid(row=2, column=0, columnspan=4)

        self.save_button.grid(row=3, column=0)
        self.exit_button.grid(row=3, column=1)
        self.saveandnew_button.grid(row=3, column=2)
        self.saveandnew_button.grid_remove()
        self.save_button.grid_remove()

    def action_save_neue_schicht(self, undneu=0):
        global assistent

        calendar = self.schicht_calendar_frame.get_data()
        beginn = calendar["beginn"]
        ende = calendar["ende"]
        asn = self.asn_frame.get_data()
        additional = self.schicht_add_options.get_data()

        # Schicht erstellen und zum Assistenten stopfen
        schicht = Schicht(beginn, ende, asn)
        schicht.ist_pcg = additional["is_pcg"]
        schicht.ist_assistententreffen = additional["is_at"]
        schicht.ist_ausfallgeld = additional["is_afg"]
        schicht.ist_kurzfristig = additional["is_rb"]

        if additional["alternative adresse start"]:
            schicht.beginn_andere_adresse = additional["alternative adresse start"]
        if additional["alternative adresse ende"]:
            schicht.beginn_andere_adresse = additional["alternative adresse ende"]

        assistent.schicht_dazu(schicht)
        alles_speichern()
        self.destroy()
        if undneu == 1:
            FensterNeueSchicht(root)


class NeuerUrlaub(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.headline = tk.Label(self, text="Urlaub eintragen")
        self.startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.urlaubsstatus = tk.StringVar()
        self.urlaubsstatus.set('notiert')
        self.status_label = tk.Label(self, text="Status")
        self.status_input_radio1 = \
            tk.Radiobutton(self, text="notiert", padx=20,
                           variable=self.urlaubsstatus, value='notiert')
        self.status_input_radio2 = \
            tk.Radiobutton(self, text="beantragt", padx=20,
                           variable=self.urlaubsstatus, value='beantragt')
        self.status_input_radio3 = \
            tk.Radiobutton(self, text="genehmigt", padx=20,
                           variable=self.urlaubsstatus, value='genehmigt')

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neuer_urlaub)
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu",
                                           command=lambda: self.action_save_neuer_urlaub(undneu=1))

        # ins Fenster packen
        self.headline.grid(row=0, column=0, columnspan=4)
        self.startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        self.enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        self.status_label.grid(row=3, column=0)

        self.status_input_radio1.grid(row=3, column=1)
        self.status_input_radio2.grid(row=3, column=2)
        self.status_input_radio3.grid(row=3, column=3)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def action_save_neuer_urlaub(self, undneu=0):
        global assistent

        startdatum = self.startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = self.enddatum_input.get_date().split('/')
        # urlaub geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)
        status = self.urlaubsstatus.get()

        # Schicht erstellen und zum Assistenten stopfen
        urlaub = Urlaub(beginn, ende, status)
        assistent.urlaub_dazu(urlaub)
        alles_speichern()
        self.destroy()
        if undneu == 1:
            NeuerUrlaub(root)


class NeueAU(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.headline = tk.Label(self, text="AU/krank eintragen")
        self.startdatum_label = tk.Label(self, text="von")
        self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.enddatum_label = tk.Label(self, text="bis")
        self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy')
        self.urlaubsstatus = tk.StringVar()
        self.urlaubsstatus.set('notiert')

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neue_arbeitsunfaehigkeit)
        self.exit_button = tk.Button(self, text="Abbrechen", command=self.destroy)
        self.saveandnew_button = tk.Button(self,
                                           text="Daten speichern und neu",
                                           command=lambda: self.action_save_neue_arbeitsunfaehigkeit(undneu=1))

        # ins Fenster packen
        self.headline.grid(row=0, column=0, columnspan=4)
        self.startdatum_label.grid(row=1, column=0)
        self.startdatum_input.grid(row=1, column=1, columnspan=2)
        self.enddatum_label.grid(row=1, column=3)
        self.enddatum_input.grid(row=1, column=4)

        self.save_button.grid(row=15, column=0)
        self.exit_button.grid(row=15, column=1)
        self.saveandnew_button.grid(row=15, column=2)

    def action_save_neue_arbeitsunfaehigkeit(self, undneu=0):
        global assistent

        startdatum = self.startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]), 0, 0)
        enddatum = self.enddatum_input.get_date().split('/')
        # au geht bis 23:59 am letzten Tag
        ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]), 23, 59)

        # au erstellen und zum Assistenten stopfen
        au = Arbeitsunfaehigkeit(beginn, ende)
        assistent.au_dazu(au)
        alles_speichern()
        self.destroy()
        if undneu == 1:
            NeueAU(root)


class Hauptfenster(tk.Frame):
    class Begruessung(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.info_text = tk.Label(self, text="Bitte erstelle oder öffne eine Assistenten-Datei")
            self.info_text.grid(row=0, column=0, columnspan=2)
            self.button_oeffnen = tk.Button(self, text="Gespeicherten Assistenten laden", command=alles_laden)
            self.button_oeffnen.grid(row=1, column=0)
            self.button_neu = tk.Button(self, text="Neuen Assistenten anlegen", command=lambda: NeuerAS(root))
            self.button_neu.grid(row=1, column=1)

        def show(self):
            self.grid()

        def hide(self):
            self.grid_remove()

    class Hauptseite(tk.Frame):
        class Title(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)
                hallo = tk.Label(self, text="Hallo " + str(assistent))
                hallo.grid(row=0, column=0)

        class Navigation(tk.Frame):
            def __init__(self, parent, offset=0):
                super().__init__(parent)
                self.parent = parent
                self.offset = offset
                # offset = 0
                vormonat = tk.Button(self, text='einen Monat Zurück', command=lambda: self.monat_change(-1))
                self.arbeitsdate = self.berechne_arbeitsdate()
                self.aktueller_monat = tk.Label(self, text=self.arbeitsdate.strftime("%B %Y"))
                naechster_monat = tk.Button(self, text='Nächster Monat', command=lambda: self.monat_change(+1))

                # in den frame packen
                vormonat.grid(row=0, column=0)
                self.aktueller_monat.grid(row=0, column=1)
                naechster_monat.grid(row=0, column=2)

            def berechne_arbeitsdate(self):
                aktuelles_datum = datetime.date.today()
                jahrmonat = divmod(aktuelles_datum.month + self.offset, 12)
                jahroffset = jahrmonat[0]
                monat = jahrmonat[1]
                if monat == 0:
                    monat = 12
                    jahroffset -= 1
                return datetime.date(aktuelles_datum.year + jahroffset, monat, 1)

            def monat_change(self, step):
                self.offset += step
                self.arbeitsdate = self.berechne_arbeitsdate()
                # Hack date in datetime übersetzen
                # TODO  konsequent datetime verwenden.
                self.arbeitsdate = datetime.datetime(self.arbeitsdate.year,
                                                     self.arbeitsdate.month,
                                                     self.arbeitsdate.day,
                                                     0, 0, 0)
                self.aktueller_monat.config(text=self.arbeitsdate.strftime("%B %Y"))
                root.fenster.hauptseite.tab.destroy()
                root.fenster.hauptseite.seitenleiste.destroy()
                root.fenster.hauptseite.seitenleiste = root.fenster.hauptseite.Seitenleiste(root.fenster.hauptseite)
                root.fenster.hauptseite.tab = root.fenster.hauptseite.Tabelle(root.fenster.hauptseite, self.arbeitsdate)

                root.fenster.hauptseite.tab.grid(row=2, column=0)
                root.fenster.hauptseite.seitenleiste.draw()
                root.fenster.hauptseite.seitenleiste.grid(row=2, column=1)

        class Tabelle(tk.Frame):
            def __init__(self,
                         parent,
                         arbeitsdatum=datetime.datetime(datetime.date.today().year,
                                                        datetime.date.today().month,
                                                        1)):
                super().__init__(parent, bd=1)
                self.start = self.arbeitsdatum = arbeitsdatum
                self.end = self.verschiebe_monate(1, arbeitsdatum)
                schichten = assistent.get_all_schichten(self.start, self.end)
                if not schichten:
                    schichten = insert_standardschichten(self.start, self.end)
                schichten_sortiert = split_schichten_um_mitternacht(schichten)
                schichten_sortiert = sort_und_berechne_schichten_by_day(schichten_sortiert, arbeitsdatum)
                # Tabelle aufbauen
                # kopfzeile erstellen
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

                # körper
                meine_tabelle = []
                spaltenzahl = 24
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
                            #  Wochentag
                            inhalt = datetime.datetime(arbeitsdatum.year, arbeitsdatum.month, zeilendaten[0]).strftime(
                                '%a')

                        elif spaltennummer == 11:
                            zeile = []
                            width = 3
                            # Tag
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
                                inhalt = ''
                                # TODO andere Lohnarten für Ausfallgeld, Berechnung Wegegeld
                                if zeilendaten[1].ist_ausfallgeld:
                                    inhalt += "Ausf."
                                if zeilendaten[1].ist_assistententreffen:
                                    inhalt += "AT "
                                if zeilendaten[1].ist_pcg:
                                    inhalt += "PCG "
                                inhalt += zeilendaten[1].asn.kuerzel
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
                                parent.seitenleiste.arbeitsstunden += austunden
                            elif assistent.check_urlaub(datetime.datetime(arbeitsdatum.year,
                                                                          arbeitsdatum.month, zeilendaten[0], 0, 1)):
                                urlaub = assistent.check_urlaub(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                                  zeilendaten[0], 0, 1))
                                ustunden = urlaub.berechne_durchschnittliche_stundenzahl_pro_tag()
                                inhalt = ustunden
                                parent.seitenleiste.arbeitsstunden += ustunden
                            elif zeilendaten[1] != 'empty':
                                parent.seitenleiste.arbeitsstunden += zeilendaten[1].stundenzahl
                                inhalt = str(zeilendaten[1].berechne_stundenzahl())
                            else:
                                inhalt = ''
                            width = 5
                        elif spaltennummer == 16:
                            if assistent.check_au(datetime.datetime(arbeitsdatum.year,
                                                                    arbeitsdatum.month, zeilendaten[0], 0, 1)):
                                au = assistent.check_au(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                          zeilendaten[0], 0, 1))
                                aulohn = au.aulohn_pro_tag
                                aulohn_pro_stunde = au.aulohn_pro_stunde
                                parent.seitenleiste.grundlohn += aulohn
                                parent.seitenleiste.grundlohn_pro_stunde = aulohn_pro_stunde
                                inhalt = "{:,.2f}€".format(aulohn)
                            elif assistent.check_urlaub(datetime.datetime(arbeitsdatum.year,
                                                                          arbeitsdatum.month, zeilendaten[0], 0, 1)):
                                urlaub = assistent.check_urlaub(datetime.datetime(arbeitsdatum.year, arbeitsdatum.month,
                                                                                  zeilendaten[0], 0, 1))
                                ulohn = urlaub.ulohn_pro_tag
                                ulohn_pro_stunde = urlaub.ulohn_pro_stunde
                                parent.seitenleiste.grundlohn += ulohn
                                parent.seitenleiste.grundlohn_pro_stunde = ulohn_pro_stunde
                                inhalt = "{:,.2f}€".format(ulohn)
                            elif zeilendaten[1] != 'empty':
                                schichtlohn = zeilendaten[1].schichtlohn
                                parent.seitenleiste.grundlohn += zeilendaten[1].schichtlohn
                                parent.seitenleiste.grundlohn_pro_stunde = zeilendaten[1].stundenlohn
                                inhalt = "{:,.2f}€".format(schichtlohn)
                            else:
                                inhalt = ''
                            width = 8
                        elif spaltennummer == 17:
                            if zeilendaten[1] != 'empty':
                                if zeilendaten[1].ist_kurzfristig:
                                    kurzfr = schichtlohn * 0.2
                                    parent.seitenleiste.kurzfr_pro_stunde = zeilendaten[1].stundenlohn * 0.2
                                    parent.seitenleiste.kurzfr_stunden = zeilendaten[1].stundenzahl
                                    parent.seitenleiste.kurzfr += kurzfr
                                    inhalt = "{:,.2f}€".format(kurzfr)
                                else:
                                    inhalt = ''
                            else:
                                inhalt = ''
                            width = 8

                        elif spaltennummer == 18:
                            if zeilendaten[1] != 'empty':
                                nachtstunden = zeilendaten[1].nachtstunden
                                # root.fenster.hauptseite.seitenleiste.nachtstunden += nachtstunden
                                inhalt = str(nachtstunden)
                            else:
                                inhalt = ''
                            width = 8
                        elif spaltennummer == 19:
                            if zeilendaten[1] != 'empty':
                                nachtzuschlag_schicht = zeilendaten[1].nachtzuschlag_schicht
                                parent.seitenleiste.nachtzuschlag += zeilendaten[1].nachtzuschlag_schicht
                                parent.seitenleiste.nachtzuschlag_pro_stunde = zeilendaten[1].nachtzuschlag
                                inhalt = "{:,.2f}€".format(nachtzuschlag_schicht)
                            else:
                                inhalt = ''
                            width = 8
                        elif spaltennummer == 20:
                            if zeilendaten[1] != 'empty' and zeilendaten[1].zuschlaege != {}:
                                grund = zeilendaten[1].zuschlaege['zuschlagsgrund']
                                zuschlag_stunden = zeilendaten[1].zuschlaege['stunden_gesamt']
                                parent.seitenleiste.zuschlaege[grund]['stunden_gesamt'] \
                                    += zuschlag_stunden
                                inhalt = str(zuschlag_stunden) + ' ' + zeilendaten[1].zuschlaege['zuschlagsgrund']
                            else:
                                inhalt = ''
                            width = 15
                        elif spaltennummer == 21:
                            if zeilendaten[1] != 'empty' and zeilendaten[1].zuschlaege != {}:
                                grund = zeilendaten[1].zuschlaege['zuschlagsgrund']
                                zuschlag_schicht = zeilendaten[1].zuschlaege['zuschlag_schicht']
                                parent.seitenleiste.zuschlaege[grund]['zuschlaege_gesamt'] \
                                    += zuschlag_schicht
                                parent.seitenleiste.zuschlaege[grund]['zuschlag_pro_stunde'] = \
                                    zeilendaten[1].zuschlaege['zuschlag_pro_stunde']
                                inhalt = "{:,.2f}€".format(zuschlag_schicht)
                            else:
                                inhalt = ''
                            width = 8
                        elif spaltennummer == 22:
                            if zeilendaten[1] != 'empty':
                                parent.seitenleiste.wechselschichtzulage += zeilendaten[
                                    1].wechselschichtzulage_schicht
                                parent.seitenleiste.wechselschichtzulage_pro_stunde = zeilendaten[
                                    1].wechselschichtzulage
                                inhalt = "{:,.2f}€".format(zeilendaten[1].wechselschichtzulage_schicht)
                            else:
                                inhalt = ''
                            width = 8

                        elif spaltennummer == 23:
                            if zeilendaten[1] != 'empty':
                                parent.seitenleiste.orga += zeilendaten[1].orgazulage_schicht
                                parent.seitenleiste.orga_pro_stunde = zeilendaten[1].orgazulage
                                inhalt = "{:,.2f}€".format(zeilendaten[1].orgazulage_schicht)
                            else:
                                inhalt = ''
                            width = 8

                        if spaltennummer < 10:
                            if zeilendaten[1] != 'empty':
                                if text != '':
                                    if command == 'kill':
                                        zelle = tk.Button(self, text=text, command=lambda: kill_schicht(key_string))
                                    elif command == 'edit':
                                        zelle = tk.Button(self, text=text)
                                    zelle.image = tk.PhotoImage(file=image, width=16, height=16)
                                    zelle.config(image=zelle.image, width=16, height=16)
                                    zelle.grid(row=zaehler, column=spaltennummer)
                                    zeile.append(zelle)

                        elif spaltennummer >= 10:
                            zelle = tk.Entry(self, width=width)
                            zelle.grid(row=zaehler, column=spaltennummer)
                            zelle.delete(0, "end")
                            zelle.insert(0, inhalt)
                            zelle.config(state='readonly')
                            zeile.append(zelle)

                    meine_tabelle.append(zeile)

            def verschiebe_monate(self, offset, datum=datetime.datetime.now()):
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

            def __init__(self, parent):
                super().__init__(parent)
                self.zuschlaege = {}
                for zuschlag_name in lohntabelle.zuschlaege.keys():
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
                brutto = self.grundlohn + self.wechselschichtzulage + self.nachtzuschlag + self.orga + self.kurzfr
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
                                   spalte1='Bruttolohn',
                                   spalte4="{:,.2f}€".format(brutto))
                zeile.grid(row=zeilenzaehler, column=0)
                zeilenzaehler += 1

        def __init__(self, parent):  # von Hauptseite
            super().__init__(parent)
            self.title = self.Title(self)
            self.nav = self.Navigation(self)
            self.seitenleiste = self.Seitenleiste(self)
            self.tab = self.Tabelle(self)

            self.title.grid(row=0, column=0, columnspan=2)
            self.nav.grid(row=1, column=0, columnspan=2)
            self.tab.grid(row=2, column=0)
            self.seitenleiste.grid(row=2, column=1)
            self.seitenleiste.draw()

        def show(self):
            self.grid()

        def hide(self):
            self.grid_remove()

    def __init__(self, parent):  # von Hauptfenster
        super().__init__(parent)
        if not assistent.assistent_is_loaded:
            self.hello = self.Begruessung(self)
            self.hello.grid(row=0, column=0)
        else:
            self.hauptseite = self.Hauptseite(self)
            self.hauptseite.grid(row=0, column=0)


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


def alles_speichern(neu=0):
    global assistent

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
        menuleiste = Menuleiste(root)
        root.config(menu=menuleiste)
    root.fenster.destroy()
    root.fenster = Hauptfenster(root)
    root.fenster.grid(row=0, column=0)


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
        # menueleiste laden
        menuleiste = Menuleiste(root)
        root.config(menu=menuleiste)

        root.fenster.destroy()
        root.fenster = Hauptfenster(root)
        root.fenster.grid(row=0, column=0)


def action_get_info_dialog():
    m_text = "\
************************\n\
Autor: Simon Beyer\n\
Date: 16.11.2020\n\
Version: 0.01\n\
************************"
    mb.showinfo(message=m_text, title="Infos")


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
    root.fenster.destroy()
    root.fenster = Hauptfenster(root)
    root.fenster.grid(row=0, column=0)


def insert_standardschichten(erster_tag, letzter_tag):
    def get_ersten_xxtag(int_weekday, erster=datetime.datetime.now()):
        for counter in range(1, 8):
            if datetime.datetime(year=erster.year, month=erster.month, day=counter, hour=0,
                                 minute=0).weekday() == int_weekday:
                return counter

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
                schicht_neu = Schicht(beginn=start, ende=end, asn=asn)
                assistent.schicht_dazu(schicht_neu)

    return assistent.get_all_schichten(erster_tag, letzter_tag)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('1200x1000')
        self.title("Dein Assistentenlohn")
        # Menue wird leer initialisiert und erst beim Laden des AS gesetzt
        self.config(menu="")

        self.fenster = Hauptfenster(self)
        self.fenster.pack()


assistent = AS()
lohntabelle = LohnTabelle()

if __name__ == "__main__":
    root = App()
    root.mainloop()
