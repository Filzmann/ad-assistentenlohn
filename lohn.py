import datetime
from helpers import Helpers


class LohnDatensatz:
    def __init__(self, erfahrungsstufe, grundlohn, zuschlaege, gueltig_ab=datetime.datetime(1970, 1, 1)):
        self.erfahrungsstufe = erfahrungsstufe
        self.eingruppierung = 5
        self.grundlohn = grundlohn
        self.zuschlaege = zuschlaege
        self.gueltig_ab = gueltig_ab

    def get_grundlohn(self):
        return self.grundlohn

    def get_erfahrungsstufe(self):
        return self.erfahrungsstufe


class LohnTabelle:
    def __init__(self, assistent):
        # EG5 Erfahrungsstufen hinzufügen
        self.assistent = assistent
        self.einstellungsdatum = assistent.einstellungsdatum
        self.erfahrungsstufen = []

        gueltig_ab = datetime.datetime(2021, 1, 1)
        self.zuschlaege = {'Nacht': 3.44, 'Samstag': 3.44, 'Sonntag': 4.30,
                           'Feiertag': 6.01, 'Wechselschicht': 0.63, 'Orga': 0.20, 'Hl. Abend': 6.01,
                           'Überstunde': 5.16, 'Silvester': 6.01}
        self.erfahrungsstufen.append(LohnDatensatz(1, 15.22, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(2, 16.47, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(3, 17.19, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.86, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(5, 18.40, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(6, 18.77, self.zuschlaege, gueltig_ab))

        gueltig_ab = datetime.datetime(2020, 1, 1)
        self.zuschlaege = {'Nacht': 3.38, 'Samstag': 3.38, 'Sonntag': 4.22,
                           'Feiertag': 5.91, 'Wechselschicht': 0.63, 'Orga': 0.20, 'Hl. Abend': 5.91,
                           'Überstunde': 4.48, 'Silvester': 5.91}
        self.erfahrungsstufen.append(LohnDatensatz(1, 14.92, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(2, 16.18, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(3, 16.89, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.56, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(5, 18.11, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(6, 18.47, self.zuschlaege, gueltig_ab))

        gueltig_ab = datetime.datetime(2019, 7, 1)
        self.zuschlaege = {'Nacht': 3.27, 'Samstag': 3.27, 'Sonntag': 4.09,
                           'Feiertag': 5.72, 'Wechselschicht': 0.63, 'Orga': 0.20, 'Hl. Abend': 5.72,
                           'Überstunde': 4.90, 'Silvester': 5.72}
        self.erfahrungsstufen.append(LohnDatensatz(1, 14.31, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(2, 15.64, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(3, 16.35, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.02, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(5, 17.56, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(6, 17.91, self.zuschlaege, gueltig_ab))

        #  ganz alt_grundsätzliche Befüllung
        self.zuschlaege = {'Nacht': 3.27, 'Samstag': 3.27, 'Sonntag': 4.09,
                           'Feiertag': 5.72, 'Wechselschicht': 0, 'Orga': 0, 'Hl. Abend': 5.72,
                           'Überstunde': 0, 'Silvester': 5.72}
        self.erfahrungsstufen.append(LohnDatensatz(1, 14.31, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(2, 15.64, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(3, 16.35, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.02, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(5, 17.56, self.zuschlaege, gueltig_ab))
        self.erfahrungsstufen.append(LohnDatensatz(6, 17.91, self.zuschlaege, gueltig_ab))

    def get_lohndatensatz_by_erfahrungsstufe(self, erfahrungsstufe, datum=datetime.datetime.now()):
        output = None
        akt_gueltig_ab = datetime.datetime(1970, 1, 1)
        for datensatz in self.erfahrungsstufen:
            if datensatz.get_erfahrungsstufe() == erfahrungsstufe and datensatz.gueltig_ab < datum:
                if datensatz.gueltig_ab > akt_gueltig_ab:
                    output = datensatz
                    akt_gueltig_ab = datensatz.gueltig_ab
        return output

    def get_grundlohn(self, datum):
        erfahrungsstufe = self.get_erfahrungsstufe(datum)
        ds = self.get_lohndatensatz_by_erfahrungsstufe(erfahrungsstufe, datum)
        return ds.get_grundlohn()

    def get_zuschlag(self, zuschlag='all', schichtdatum=datetime.datetime.now()):
        erfahrungsstufe = self.get_erfahrungsstufe(schichtdatum)
        ds = self.get_lohndatensatz_by_erfahrungsstufe(erfahrungsstufe=erfahrungsstufe, datum=schichtdatum)
        if zuschlag == 'all':
            return ds.zuschlaege
        else:
            return ds.zuschlaege[zuschlag]

    def get_erfahrungsstufe(self, datum=datetime.datetime.now()):

        delta = Helpers.get_duration(self.assistent.einstellungsdatum, datum, 'years')
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
