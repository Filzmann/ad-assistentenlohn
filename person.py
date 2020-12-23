import datetime
import pickle
from lohn import LohnTabelle
import tkinter.filedialog as filedialog
from arbeitszeit import Schicht


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


class Weg:
    def __init__(self, address1: Adresse, address2: Adresse, reisezeit_minuten: int, entfernung_km: float):
        self.address1 = address1
        self.address2 = address2
        self.reisezeit_minuten = reisezeit_minuten
        self.entfernung_km = entfernung_km


# erstellt den einen AS, kommt genau einmal pro Datei vor
class AS(Person):
    count = 0
    assistent_is_loaded = 0

    def __init__(self, name='', vorname='', email="keine@email.de",
                 einstellungsdatum=datetime.datetime(1970, 1, 1, 0, 0, 0)):
        self.filepath = ''
        self.lohntabelle = LohnTabelle(self)
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
        self.letzte_eingetragene_schicht = Schicht(beginn=datetime.datetime.now(),
                                                   ende=datetime.datetime.now(),
                                                   asn="Neuer ASN", assistent=self)

        self.adressen = []
        self.wege = []
        # TODO in Config auslagern
        self.adressen.append(Adresse(kuerzel="Hauptstelle - Urbanstraße", strasse="Urbanstr.",
                                     hnr="100", plz="10967", stadt="Berlin"))
        self.adressen.append(Adresse(kuerzel="Südbüro - Mehringhof", strasse="Gneisenaustr.",
                                     hnr="2a", plz="10961", stadt="Berlin"))
        self.adressen.append(Adresse(kuerzel="NO-W-BR-Büro", strasse="Wilhelm-Kabus-Str.",
                                     hnr="27-30", plz="10829", stadt="Berlin"))
        self.bruttoloehne = {}

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

    def get_all_schichten(self, start: datetime.datetime = 0, end: datetime.datetime = 0):
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

    def delete_urlaub(self, datum: datetime.datetime):
        for urlaub in self.urlaub:
            if urlaub.beginn <= datum <= urlaub.ende:
                self.urlaub.remove(urlaub)
                return True

    def delete_au(self, datum: datetime.datetime):
        for arbeitsunfaehigkeit in self.au:
            if arbeitsunfaehigkeit.beginn <= datum <= arbeitsunfaehigkeit.ende:
                self.au.remove(arbeitsunfaehigkeit)
                return True

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

    def load_from_file(self):
        files = [('Assistenten-Dateien', '*.dat')]
        dateiname = filedialog.askopenfilename(filetypes=files, defaultextension=files)
        assistent = None
        if not dateiname == '':
            self.set_filepath(dateiname)
            infile = open(dateiname, 'rb')
            assistent = pickle.load(infile)
            infile.close()
            assistent.set_filepath(dateiname)
            self.__class__.assistent_is_loaded = 1

        return assistent

    def save_to_file(self, neu=0):
        if neu == 1:
            files = [('Assistenten-Dateien', '*.dat')]
            dateiname = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
            dateiname = dateiname.name
            self.set_filepath(dateiname)
            self.__class__.assistent_is_loaded = 1
        else:
            dateiname = self.get_filepath()
        outfile = open(dateiname, 'wb')
        pickle.dump(self, outfile)
        outfile.close()
        return self

    # TODO optimieren
    def get_pfk_by_string(self, string):
        data = string.split()
        for pfk in self.pfk_liste:
            if pfk.vorname == data[0]:
                if len(data) > 1:
                    if pfk.name == data[1]:
                        return pfk
                return pfk

    def get_fahrtzeit(self, adresse1: Adresse, adresse2: Adresse):
        for weg in self.wege:
            if (weg.adresse1 == adresse1 and weg.adresse2 == adresse2) \
                    or (weg.adresse1 == adresse2 and weg.adresse2 == adresse1):
                return weg.reisezeit_minuten
        return 0

    def get_km(self, adresse1: Adresse, adresse2: Adresse):
        for weg in self.wege:
            if (weg.adresse1 == adresse1 and weg.adresse2 == adresse2) \
                    or (weg.adresse1 == adresse2 and weg.adresse2 == adresse1):
                return weg.entfernung_km
        return 0

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
        self.adressen = []
        self.home = Adresse(kuerzel='zu Hause', strasse=strasse, hnr=hausnummer, plz=plz, stadt=stadt)
        self.adressen.append(self.home)
        self.schicht_templates = []
        self.eb = EB('', '', '')
        self.pfk = PFK('', '', '')

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
