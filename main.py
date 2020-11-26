import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
# import shelve
import pickle
import datetime
from tkcalendar import Calendar
import copy


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

    def __init__(self, name='', vorname='', email="keine@email.de", einstellungsdatum="01.01.1970"):
        self.filepath = ''
        self.schichten = {}
        self.asn = {}
        self.name = name
        self.vorname = vorname
        self.email = email
        self.einstellungsdatum = einstellungsdatum
        self.__class__.count += 1
        self.festeSchichten = {}
        self.urlaub = {}
        self.arbeitsunfaehig = {}

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

    # TODO funktion get_asn_by_kuerzel implementieren
    def get_asn_by_kuerzel(self, kuerzel):
        return self.asn[kuerzel]

    def get_all_schichten(self, start=0, end=0):
        """ wenn keine datetimes für start und end angegeben sind, werden alle Schichten ausgegeben,
         ansonsten alle schichten, die größer als start und <= end sind """
        if start == 0 and end == 0:
            return self.schichten
        else:
            ausgabe = {}
            for schicht in self.schichten.values():
                beginn_akt_schicht = schicht.get_beginn()
                end_akt_schicht = schicht.get_ende()
                if start <= beginn_akt_schicht < end or start <= end_akt_schicht < end:
                    ausgabe[beginn_akt_schicht.strftime("%Y%m%d%H%M")] = schicht
            return ausgabe

    def set_all_schichten(self, schichten):
        """ Nimmt ein dict von Schichten entgegen und weist diese dem AS zu"""
        self.schichten = schichten

    def asn_dazu(self, asn):
        self.asn[asn.get_kuerzel()] = asn

    def schicht_dazu(self, schicht):
        key = schicht.get_beginn().strftime("%Y%m%d%H%M")
        self.schichten[key] = schicht


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


class Schicht:
    beginn = datetime
    end = datetime
    asn = ASN

    def __init__(self, beginn, ende, asn):
        self.beginn = beginn
        self.ende = ende
        self.asn = asn

    def __str__(self):
        return self.asn.get_kuerzel() + " - " + self.beginn.strftime("%m/%d/%Y, %H:%M") + ' bis ' + \
               self.ende.strftime("%m/%d/%Y, %H:%M")

    def get_beginn(self):
        return self.beginn

    def set_beginn(self, beginn):
        self.beginn = beginn

    def get_ende(self):
        return self.ende

    def split_by_null_uhr(self):
        ausgabe = []
        if self.beginn.strftime("%Y%m%d") == self.ende.strftime("%Y%m%d"):
            ausgabe.append(Schicht(self.beginn, self.ende, self.asn))
        else:
            rest = dict(start=self.beginn, ende=self.ende)
            while rest['start'] <= rest['ende']:
                r_start = rest['start']
                neuer_start_rest_y = int(r_start.strftime('%Y'))
                neuer_start_rest_m = int(r_start.strftime('%m'))
                neuer_start_rest_d = int(r_start.strftime('%d'))
                neuer_start_rest = datetime.datetime(neuer_start_rest_y, neuer_start_rest_m, neuer_start_rest_d + 1)
                if neuer_start_rest <= rest['ende']:
                    ausgabe.append(Schicht(rest['start'], neuer_start_rest, self.asn))
                else:
                    ausgabe.append(Schicht(rest['start'], rest['ende'], self.asn))

                rest['start'] = neuer_start_rest

        return ausgabe

    def set_ende(self, ende):
        self.ende = ende

    def get_asn(self):
        return self.asn

    def berechne_stundenzahl(self):
        diff = self.ende - self.beginn
        sekunden = diff.total_seconds()
        stunden = sekunden / 3600
        return stunden


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
        gueltig_ab = datetime.date(2020, 1, 1)
        # EG5 Erfahrungsstufen hinzufügen
        self.erfahrungsstufen = []
        zuschlaege = {'nacht': 3.38, 'samstag': 3.38, 'sonnstag': 4.22,
                      'feiertag': 22.80, 'wechselschicht': 0.63, 'WeihSyl': 5.72, 'Überstunde': 4.48}
        self.erfahrungsstufen.append(LohnDatensatz(1, 14.92, zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(2, 16.18, zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(3, 16.89, zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(4, 17.56, zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(5, 18.11, zuschlaege))
        self.erfahrungsstufen.append(LohnDatensatz(6, 18.47, zuschlaege))

    def get_lohndatensatz_by_erfahrungsstufe(self, erfahrungsstufe):
        for datensatz in self.erfahrungsstufen:
            if datensatz.get_erfahrungsstufe() == erfahrungsstufe:
                return datensatz

    def get_grundlohn(self):
        erfahrungsstufe = self.get_erfahrungsstufe()
        ds = self.get_lohndatensatz_by_erfahrungsstufe(erfahrungsstufe)
        return ds.get_grundlohn()

    def get_erfahrungsstufe(self):
        # einstieg mit 1
        # nach 1 Jahr insgesamt 2
        # nach 3 jahren insgesamt 3
        # nach 6 jahren insg. 4
        # nach 10 Jahren insg. 5
        # nach 15 Jahren insg. 6
        return 4


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
            if tag == int(schicht.get_beginn().strftime('%d')):
                paar = [tag, schicht]
                ausgabe.append(paar)
                tag_isset = 1
        if tag_isset == 0:
            ausgabe.append([tag, 'empty'])

    return ausgabe


def neuer_as():
    def action_save_neuer_as():
        global assistent
        assistent = AS(form_neuer_as_nachname_input.get(), form_neuer_as_vorname_input.get(),
                       form_neuer_as_email_input.get(), form_neuer_as_einstellungsdatum_input.get_date())
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
        # print(value)
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

    def action_save_neue_schicht():
        global assistent

        startdatum = form_neue_schicht_startdatum_input.get_date().split('/')
        beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                   int(form_neue_schicht_startzeit_input.hourstr.get()),
                                   int(form_neue_schicht_startzeit_input.minstr.get()))

        # ende der Schicht bestimmen. Fälle: Tagschicht, Nachtschicht, Reise
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
        # print(assistent)
        schicht = Schicht(beginn, ende, asn)
        # print(schicht)
        assistent.schicht_dazu(schicht)
        alles_speichern()
        fenster_neue_schicht.destroy()

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

    help_menu.add_command(label="Info!", command=action_get_info_dialog)

    # Nun fügen wir die Menüs (Datei und Help) der Menüleiste als
    # "Drop-Down-Menü" hinzu
    menuleiste.add_cascade(label="Datei", menu=datei_menu)
    menuleiste.add_cascade(label="Bearbeiten", menu=bearbeiten_menu)
    menuleiste.add_cascade(label="Help", menu=help_menu)
    # Die Menüleiste mit den Menüeinträgen noch dem Fenster übergeben und fertig.
    root.config(menu=menuleiste)


def split_schichten_um_mitternacht(splitschichten):
    """Diese Funktion teilt Nachtschichten und mehrtägige Schichten an der null Uhr Grenze auf
    Sie liefert Schichten in der Form eines dicts[YYYYmmddHHMM]->schicht zurück """
    # TODO implement
    ausgabe = []
    for schicht in splitschichten:
        val = splitschichten[schicht]
        liste = val.split_by_null_uhr()
        for splitschicht in liste:
            ausgabe.append(splitschicht)
    return ausgabe


def zeichne_hauptseite():
    global button_neu, button_oeffnen, assistent

    def erstelle_navigation():
        for navwidget in nav.winfo_children():
            navwidget.destroy()
        vormonat = tk.Button(nav, text='einen Monat Zurück')
        aktuelles_datum = datetime.date.today()
        aktueller_monat = tk.Label(nav, text=aktuelles_datum.strftime("%B %Y"))
        naechster_monat = tk.Button(nav, text='Nächster Monat')

        # in den frame packen
        vormonat.grid(row=0, column=0)
        aktueller_monat.grid(row=0, column=1)
        naechster_monat.grid(row=0, column=2)

    def erstelle_tabelle(monatjahr=datetime.date.today()):
        for tabwidget in tabelle.winfo_children():
            tabwidget.destroy()
        monat = int(monatjahr.strftime('%m'))
        jahr = int(monatjahr.strftime('%Y'))
        start = datetime.datetime(jahr, monat, 1, 0, 0, 0)
        end = datetime.datetime(jahr, monat + 1, 1, 0, 0, 0)
        schichten = assistent.get_all_schichten(start, end)
        # nicht die schichten des AS kaputtmachen, daher Kopie
        schichten_copy = copy.deepcopy(schichten)
        schichten_sortiert = split_schichten_um_mitternacht(schichten_copy)
        schichten_sortiert = sort_und_berechne_schichten_by_day(schichten_sortiert)

        # Tabelle aufbauen
        # kopfzeile erstellen
        tk.Label(tabelle, text='Tag', borderwidth=1, relief="solid", width=6).grid(row=0, column=0, columnspan=2)
        tk.Label(tabelle, text='von', borderwidth=1, relief="solid", width=5).grid(row=0, column=2)
        tk.Label(tabelle, text='bis', borderwidth=1, relief="solid", width=5).grid(row=0, column=3)
        tk.Label(tabelle, text='ASN', borderwidth=1, relief="solid", width=8).grid(row=0, column=4)
        tk.Label(tabelle, text='Std', borderwidth=1, relief="solid", width=5).grid(row=0, column=5)
        tk.Label(tabelle, text='Grundlohn', borderwidth=1, relief="solid", width=8).grid(row=0, column=6)

        # körper
        meine_tabelle = []
        spaltenzahl = 7
        zaehler = 0
        for zeilendaten in schichten_sortiert:
            zeile = []

            zaehler += 1
            for spaltennummer in range(0, spaltenzahl):
                if spaltennummer == 0:
                    zeile = []
                    width = 4
                    # TODO timezone checken
                    inhalt = datetime.datetime(jahr, monat, zeilendaten[0], ).strftime('%a')

                elif spaltennummer == 1:
                    zeile = []
                    width = 3
                    inhalt = zeilendaten[0]
                elif spaltennummer == 2:
                    if zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].get_beginn().strftime('%H:%M')
                    else:
                        inhalt = ''
                    width = 5
                elif spaltennummer == 3:
                    if zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].get_ende().strftime('%H:%M')
                    else:
                        inhalt = ''
                    width = 5

                elif spaltennummer == 4:
                    if zeilendaten[1] != 'empty':
                        inhalt = zeilendaten[1].get_asn().get_kuerzel()
                    else:
                        inhalt = ''
                    width = 10

                elif spaltennummer == 5:
                    if zeilendaten[1] != 'empty':
                        inhalt = str(zeilendaten[1].berechne_stundenzahl())
                    else:
                        inhalt = ''
                    width = 5
                elif spaltennummer == 6:
                    if zeilendaten[1] != 'empty':
                        print(lohntabelle.get_grundlohn())
                        inhalt = "{:,.2f}€".format(round(zeilendaten[1].berechne_stundenzahl() * lohntabelle.get_grundlohn(),2))
                    else:
                        inhalt = ''
                    width = 8

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

    if assistent.assistent_is_loaded == 1:
        hallo = tk.Label(fenster, text="Hallo " + str(assistent))
        hallo.pack()

    erstelle_navigation()
    nav.pack()
    erstelle_tabelle()
    tabelle.pack()
    # 2 Frames Für Navigation und Tabelle


assistent = AS()
lohntabelle = LohnTabelle()
root = tk.Tk()
root.geometry('1000x1000')
root.title("Dein Assistentenlohn")

fenster = tk.Frame(root)
fenster.pack()
info_text = tk.Label(fenster, text="Bitte erstelle oder öffne eine Assistenten-Datei")
info_text.pack()
button_oeffnen = tk.Button(fenster, text="Gespeicherten Assistenten laden", command=alles_laden)
button_oeffnen.pack()
button_neu = tk.Button(fenster, text="Neuen Assistenten anlegen", command=neuer_as)
button_neu.pack()

fenster.mainloop()
