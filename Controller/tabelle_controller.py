from datetime import datetime, timedelta

from sqlalchemy import or_, desc
from sqlalchemy.future import select

from Model.assistent import Assistent
from Model.lohn import Lohn
from Model.schicht import Schicht
from View.tabelle_view import TabelleView


def check_mehrtaegig(schicht):
    pseudoende = schicht.ende - timedelta(minutes=2)
    if schicht.beginn.strftime("%Y%m%d") == pseudoende.strftime("%Y%m%d"):
        return 0
    else:
        return 1


def get_duration(then, now=datetime.now(), interval="default"):
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

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]),
                                                                                                   int(d[0]),
                                                                                                   int(h[0]),
                                                                                                   int(m[0]),
                                                                                                   int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': total_duration()
    }[interval]


def split_by_null_uhr(schicht):
    ausgabe = []
    if check_mehrtaegig(schicht):
        rest = dict(start=schicht.beginn, ende=schicht.ende)
        while rest['start'] <= rest['ende']:
            r_start = rest['start']
            neuer_start_rest_y = int(r_start.strftime('%Y'))
            neuer_start_rest_m = int(r_start.strftime('%m'))
            neuer_start_rest_d = int(r_start.strftime('%d'))
            neuer_start_rest = datetime(neuer_start_rest_y,
                                        neuer_start_rest_m,
                                        neuer_start_rest_d
                                        ) + timedelta(days=1)

            if neuer_start_rest <= rest['ende']:
                ausgabe.append(Schicht(beginn=rest['start'],
                                       ende=neuer_start_rest,
                                       asn=schicht.asn,
                                       assistent=schicht.assistent,
                                       original_id=schicht.id))
            else:
                ausgabe.append(Schicht(beginn=rest['start'],
                                       ende=rest['ende'],
                                       asn=schicht.asn,
                                       assistent=schicht.assistent,
                                       original_id=schicht.id))

            rest['start'] = neuer_start_rest
    else:
        ausgabe.append(schicht)

    return ausgabe


def get_erfahrungsstufe(assistent, datum=datetime.now()):
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


def berechne_stunden(schicht):
    return get_duration(schicht.beginn, schicht.ende, "minutes") / 60


class TabelleController:
    def __init__(self, parent_controller, session, parent_view, assistent):
        self.assistent = assistent
        self.session = session
        self.parent_view = parent_view
        # initialisierung
        self.start = datetime(year=datetime.now().year,
                              month=datetime.now().month,
                              day=1)
        self.end = self.verschiebe_monate(offset=1, datum=self.start)
        letzter_tag = (self.end - timedelta(seconds=1)).day

        data = self.calculate()
        self.view = TabelleView(parent_view=parent_view,
                                data=data,
                                anzahl_tage=letzter_tag,
                                start=self.start)

    def change_arbeitsdatum(self, datum):
        self.start = datetime(year=datum.year,
                              month=datum.month,
                              day=1)
        self.end = self.verschiebe_monate(offset=1, datum=self.start)
        data = self.calculate()

        letzter_tag = (self.end - timedelta(seconds=1)).day
        self.view.draw(data=data,
                       anzahl_tage=letzter_tag,
                       start=self.start)

    def calculate(self):
        schichten = self.get_sliced_schichten(start=self.start, end=self.end)
        schichten_view_data = {}
        for schicht in schichten:
            if not schicht.beginn.strftime('%d') in schichten_view_data.keys():
                schichten_view_data[schicht.beginn.strftime('%d')] = []

            # at etc
            asn_add = ''
            asn_add += 'AT ' if schicht.ist_assistententreffen else ''
            asn_add += 'PCG ' if schicht.ist_pcg else ''
            asn_add += 'RB/BSD ' if schicht.ist_kurzfristig else ''
            asn_add += 'AFG ' if schicht.ist_ausfallgeld else ''

            # stunden
            stunden = berechne_stunden(schicht)

            lohn = self.get_lohn(assistent=self.assistent, datum=schicht.beginn)

            nachtstunden = self.get_nachtstunden(schicht)

            schichten_view_data[schicht.beginn.strftime('%d')].append(
                {
                    'schicht_id': schicht.original_id if schicht.original_id else schicht.id,
                    'von': schicht.beginn.strftime('%H:%M'),
                    'bis': schicht.ende.strftime('%H:%M'),
                    'asn': asn_add + schicht.asn.kuerzel,
                    'stunden': stunden,
                    'stundenlohn': "{:,.2f}€".format(lohn.grundlohn),
                    'schichtlohn': "{:,.2f}€".format(lohn.grundlohn * stunden),
                    'bsd': "{:,.2f}€".format(lohn.grundlohn * stunden * 0.2) if schicht.ist_kurzfristig else 0,
                    'orgazulage': "{:,.2f}€".format(lohn.orga_zuschlag),
                    'orgazulage_schicht': "{:,.2f}€".format(lohn.orga_zuschlag * stunden),
                    'wechselzulage': "{:,.2f}€".format(lohn.wechselschicht_zuschlag),
                    'wechselzulage_schicht': "{:,.2f}€".format(lohn.wechselschicht_zuschlag * stunden),
                    'nachtstunden': nachtstunden,
                    'nachtzuschlag': "{:,.2f}€".format(lohn.nacht_zuschlag),
                    'nachtzuschlag_schicht': "{:,.2f}€".format(lohn.nacht_zuschlag * nachtstunden),
                    'zuschlaege': 'nüscht'
                }
            )
        return schichten_view_data

    def get_sliced_schichten(self, start, end):
        sliced_schichten = []
        for schicht in self.session.query(Schicht).filter(
                or_(
                    Schicht.beginn.between(start, end),
                    Schicht.ende.between(start, end)
                )
        ):
            sliced_schichten += split_by_null_uhr(schicht)

        return sliced_schichten

        # TODO Urlaub und AU auch hier splitten

    @staticmethod
    def verschiebe_monate(offset, datum=datetime.now()):
        arbeitsmonat = datum.month + offset
        tmp = divmod(arbeitsmonat, 12)
        offset_arbeitsjahr = tmp[0]
        arbeitsmonat = tmp[1]
        if arbeitsmonat == 0:
            arbeitsmonat = 12
            offset_arbeitsjahr -= 1
        if offset_arbeitsjahr < 0:
            # modulo einer negativen Zahl ist ein Arschloch..hoffentlich stimmts
            arbeitsmonat = 12 - arbeitsmonat
        arbeitsjahr = datum.year + offset_arbeitsjahr
        arbeitsdatum = datetime(arbeitsjahr, arbeitsmonat, 1, 0, 0, 0)
        return arbeitsdatum

    def get_lohn(self, assistent, datum):
        erfahrungsstufe = get_erfahrungsstufe(assistent=assistent, datum=datum)
        for lohn in self.session.query(Lohn).filter(
                Lohn.erfahrungsstufe == erfahrungsstufe).filter(
            Lohn.gueltig_ab < datum).filter(
            Lohn.eingruppierung == 5
        ).order_by(desc(Lohn.gueltig_ab)).limit(1):
            return lohn
        return False

    def get_nachtstunden(self, schicht):
        return 0
