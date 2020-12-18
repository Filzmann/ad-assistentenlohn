import datetime
from helpers import Helpers


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
    def __init__(self, assistent):
        # EG5 Erfahrungsstufen hinzufügen
        self.assistent = assistent
        self.erfahrungsstufen = []
        self.zuschlaege = {'Nacht': 3.38, 'Samstag': 3.38, 'Sonntag': 4.22,
                           'Feiertag': 22.80, 'Wechselschicht': 0.63, 'Orga': 0.20, 'Hl. Abend': 5.72,
                           'Überstunde': 4.48, 'Silvester': 5.72}
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
