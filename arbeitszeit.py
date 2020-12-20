import datetime
from helpers import Helpers


# ToDo Klassen schicht, Urlaub, Krank als hierarchische Klassen vereinen schicht erbt von urlaub erbt von au
class Schicht:
    def __init__(self, beginn, ende, asn, assistent, original='root'):
        self.beginn = beginn
        self.ende = ende
        self.asn = asn
        self.assistent = assistent
        self.original_schicht = original
        self.stundenzahl = self.berechne_stundenzahl()
        self.stundenlohn = assistent.lohntabelle.get_grundlohn(self.beginn)
        self.schichtlohn = self.stundenzahl * self.stundenlohn
        self.wechselschichtzulage = assistent.lohntabelle.get_zuschlag('Wechselschicht', beginn)
        self.wechselschichtzulage_schicht = self.wechselschichtzulage * self.stundenzahl
        self.orgazulage = assistent.lohntabelle.get_zuschlag('Orga', beginn)
        self.orgazulage_schicht = self.orgazulage * self.stundenzahl
        self.nachtstunden = self.berechne_anzahl_nachtstunden()
        self.nachtzuschlag = assistent.lohntabelle.get_zuschlag('Nacht', beginn)
        self.nachtzuschlag_schicht = self.nachtstunden * self.nachtzuschlag
        self.zuschlaege = self.berechne_sa_so_weisil_feiertagszuschlaege()
        self.ist_kurzfristig = 0
        self.ist_ausfallgeld = 0
        self.ist_assistententreffen = 0
        self.ist_pcg = 0
        self.ist_schulung = 0
        self.beginn_andere_adresse = None
        self.ende_andere_adresse = None

        if self.check_mehrtaegig() == 1:
            self.teilschichten = self.split_by_null_uhr()
        else:
            self.teilschichten = []

    def __str__(self):
        return self.asn.get_kuerzel() + " - " + self.beginn.strftime("%m/%d/%Y, %H:%M") + ' bis ' + \
               self.ende.strftime("%m/%d/%Y, %H:%M")

    def calculate(self):
        self.stundenzahl = self.berechne_stundenzahl()
        self.stundenlohn = self.assistent.lohntabelle.get_grundlohn(self.beginn)
        self.schichtlohn = self.stundenzahl * self.stundenlohn
        self.wechselschichtzulage = self.assistent.lohntabelle.get_zuschlag('Wechselschicht', self.beginn)
        self.wechselschichtzulage_schicht = self.wechselschichtzulage * self.stundenzahl
        self.orgazulage = self.assistent.lohntabelle.get_zuschlag('Orga', self.beginn)
        self.orgazulage_schicht = self.orgazulage * self.stundenzahl
        self.nachtstunden = self.berechne_anzahl_nachtstunden()
        self.nachtzuschlag = self.assistent.lohntabelle.get_zuschlag('Nacht', self.beginn)
        self.nachtzuschlag_schicht = self.nachtstunden * self.nachtzuschlag
        self.zuschlaege = self.berechne_sa_so_weisil_feiertagszuschlaege()
        if self.check_mehrtaegig() == 1:
            self.teilschichten = self.split_by_null_uhr()
        else:
            self.teilschichten = []

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
                neuer_start_rest = datetime.datetime(neuer_start_rest_y,
                                                     neuer_start_rest_m,
                                                     neuer_start_rest_d) + datetime.timedelta(days=1)

                if neuer_start_rest <= rest['ende']:
                    ausgabe.append(Schicht(beginn=rest['start'],
                                           ende=neuer_start_rest,
                                           asn=self.asn,
                                           assistent=self.assistent,
                                           original=self.beginn.strftime('%Y%m%d%H%M')))
                else:
                    ausgabe.append(Schicht(beginn=rest['start'],
                                           ende=rest['ende'],
                                           asn=self.asn,
                                           assistent=self.assistent,
                                           original=self.beginn.strftime('%Y%m%d%H%M')))

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
                    nachtstunden += Helpers.get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60

                elif sechs_uhr <= teilschicht.ende <= einundzwanzig_uhr:
                    # schicht endet nach 6 uhr aber vor 21 uhr
                    nachtstunden += Helpers.get_duration(teilschicht.beginn, sechs_uhr, 'minutes') / 60

                else:
                    # schicht beginnt vor 6 uhr und geht über 21 Uhr hinaus
                    # das bedeutet ich ziehe von der kompletten schicht einfach die 15 Stunden Tagschicht ab.
                    # es bleibt der Nacht-Anteil
                    nachtstunden += Helpers.get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60 - 15
            # schicht beginnt zwischen 6 und 21 uhr
            elif sechs_uhr <= teilschicht.beginn <= einundzwanzig_uhr:
                # fängt am tag an, geht aber bis in die nachtstunden
                if teilschicht.ende > einundzwanzig_uhr:
                    nachtstunden += Helpers.get_duration(einundzwanzig_uhr, teilschicht.ende, 'minutes') / 60
            else:
                # schicht beginnt nach 21 uhr - die komplette schicht ist in der nacht
                nachtstunden += Helpers.get_duration(teilschicht.beginn, teilschicht.ende, 'minutes') / 60
        return nachtstunden

    def berechne_sa_so_weisil_feiertagszuschlaege(self):
        feiertagsstunden = 0
        feiertagsstunden_steuerfrei = 0
        feiertagsstunden_steuerpflichtig = 0
        feiertagsarray = {}
        zuschlagsgrund = ''

        test = self.check_feiertag()

        if self.check_feiertag() != '':
            if self.check_mehrtaegig() == 1:
                for teilschicht in self.teilschichten:
                    if teilschicht.check_feiertag() != '':
                        feiertagsstunden += teilschicht.berechne_stundenzahl
            else:
                feiertagsstunden = self.berechne_stundenzahl()

            zuschlag = self.assistent.lohntabelle.get_zuschlag(schichtdatum=self.beginn, zuschlag='Feiertag')
            feiertagsarray = {'zuschlagsgrund': 'Feiertag',
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': feiertagsstunden,
                              'stunden_steuerpflichtig': 0,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': feiertagsstunden * zuschlag,
                              'add_info': self.check_feiertag()
                              }
        elif datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                datetime.date(self.beginn.year, 12, 24) or \
                datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                datetime.date(self.beginn.year, 12, 31):
            if datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                    datetime.date(self.beginn.year, 12, 24):
                zuschlagsgrund = 'Hl. Abend'
            if datetime.date(self.beginn.year, self.beginn.month, self.beginn.day) == \
                    datetime.date(self.beginn.year, 12, 31):
                zuschlagsgrund = 'Silvester'

            sechsuhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 6, 0, 0)
            vierzehn_uhr = datetime.datetime(self.beginn.year, self.beginn.month, self.beginn.day, 14, 0, 0)

            if self.beginn < sechsuhr:
                if self.ende <= sechsuhr:
                    feiertagsstunden_steuerfrei = feiertagsstunden_steuerpflichtig = 0
                elif sechsuhr < self.ende <= vierzehn_uhr:
                    feiertagsstunden_steuerpflichtig = Helpers.get_duration(self.ende, sechsuhr, 'hours')
                    feiertagsstunden_steuerfrei = 0
                elif vierzehn_uhr < self.ende:
                    feiertagsstunden_steuerpflichtig = 8
                    feiertagsstunden_steuerfrei = Helpers.get_duration(vierzehn_uhr, self.ende, 'hours')
            elif sechsuhr <= self.beginn:
                if self.ende <= vierzehn_uhr:
                    feiertagsstunden_steuerpflichtig = Helpers.get_duration(self.ende, self.beginn, 'hours')
                    feiertagsstunden_steuerfrei = 0
                elif vierzehn_uhr < self.ende:
                    feiertagsstunden_steuerpflichtig = Helpers.get_duration(self.beginn, vierzehn_uhr, 'hours')
                    feiertagsstunden_steuerfrei = Helpers.get_duration(vierzehn_uhr, self.ende, 'hours')

            zuschlag = self.assistent.lohntabelle.get_zuschlag(zuschlag=zuschlagsgrund, schichtdatum=self.beginn)
            feiertagsstunden = feiertagsstunden_steuerfrei + feiertagsstunden_steuerpflichtig
            feiertagsarray = {'zuschlagsgrund': zuschlagsgrund,
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': feiertagsstunden_steuerfrei,
                              'stunden_steuerpflichtig': feiertagsstunden_steuerpflichtig,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': feiertagsstunden * zuschlag,
                              'add_info': '13:00 - 21:00 Uhr'
                              }
        elif self.beginn.weekday() == 6:
            feiertagsstunden = self.berechne_stundenzahl()
            zuschlag = self.assistent.lohntabelle.get_zuschlag(zuschlag='Sonntag', schichtdatum=self.beginn)
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
                    feiertagsstunden = Helpers.get_duration(dreizehn_uhr, self.ende, 'hours')
                else:  # self.ende > einundzwanzig_uhr:
                    feiertagsstunden = 8  # 21 - 13
            elif dreizehn_uhr <= self.beginn < einundzwanzig_uhr:
                if self.ende < einundzwanzig_uhr:
                    feiertagsstunden = self.berechne_stundenzahl()
                elif self.ende > einundzwanzig_uhr:
                    feiertagsstunden = Helpers.get_duration(self.beginn, einundzwanzig_uhr, 'hours')
            else:
                feiertagsstunden = 0

            zuschlag = self.assistent.lohntabelle.get_zuschlag(zuschlag='Samstag', schichtdatum=self.beginn)
            feiertagsarray = {'zuschlagsgrund': 'Samstag',
                              'stunden_gesamt': feiertagsstunden,
                              'stunden_steuerfrei': 0,
                              'stunden_steuerpflichtig': feiertagsstunden,
                              'zuschlag_pro_stunde': zuschlag,
                              'zuschlag_schicht': float(feiertagsstunden) * zuschlag,
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

        if tmp > 31:  # Monat erhöhen, tmp=tag erniedriegen
            m = tmp // 31
            if tmp == 31:
                m = 0
            tmp = tmp - 31

        return datetime.date(jahr, 3 + m, tmp)


class Urlaub:
    def __init__(self, beginn, ende, assistent, status='notiert'):
        self.assistent = assistent
        self.beginn = beginn
        self.ende = ende
        # status 3 Möglichkeiten: notiert, beantragt, genehmigt
        self.status = status
        self.stundenzahl = self.berechne_durchschnittliche_stundenzahl_pro_tag()['stunden']
        # todo Änderung des Stundensatzes während des Urlaubes
        self.ulohn_pro_stunde = self.berechne_durchschnittliche_stundenzahl_pro_tag()['lohn']
        self.ulohn_pro_tag = self.stundenzahl * self.ulohn_pro_stunde
        schichten = assistent.get_all_schichten(start=beginn, end=ende)
        for schicht in schichten:
            assistent.delete_schicht(key=schicht)

    def berechne_durchschnittliche_stundenzahl_pro_tag(self):

        keys = []
        date = datetime.date(self.beginn.year, self.beginn.month, 1)
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

        schnitt_stundenlohn = summe_brutto/summe_stunden
        # wir rechnen mit durchschnittlich 30 Tage pro Monat
        schnitt_stunden_pro_tag = summe_stunden/(30 * anzahl_monate)

        return {'stunden': schnitt_stunden_pro_tag, 'lohn': schnitt_stundenlohn}


class Arbeitsunfaehigkeit:
    def __init__(self, beginn, ende, assistent):
        self.beginn = beginn
        self.ende = ende
        self.assistent = assistent

        self.stundenzahl = self.berechne_durchschnittliche_stundenzahl_pro_tag()['stunden']
        # todo Änderung des Stundensatzes während des Urlaubes
        self.aulohn_pro_stunde = self.berechne_durchschnittliche_stundenzahl_pro_tag()['lohn']
        self.aulohn_pro_tag = self.stundenzahl * self.aulohn_pro_stunde
        schichten = assistent.get_all_schichten(start=beginn, end=ende)
        for schicht in schichten:
            assistent.delete_schicht(key=schicht)



    def berechne_durchschnittliche_stundenzahl_pro_tag(self):

        keys = []
        date = datetime.date(self.beginn.year, self.beginn.month, 1)
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

        return {'stunden': schnitt_stunden_pro_tag, 'lohn': schnitt_stundenlohn}
