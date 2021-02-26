from datetime import datetime, timedelta
from time import strptime

from sqlalchemy import func, desc, or_

from Model.arbeitsunfaehigkeit import AU
from Model.brutto import Brutto
from Model.lohn import Lohn
from Model.schicht import Schicht
from Model.urlaub import Urlaub


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
                ausgabe.append({'beginn': rest['start'],
                                'ende': neuer_start_rest,
                                'asn': schicht.asn,
                                'assistent': schicht.assistent,
                                'schicht_id': schicht.id,
                                'ist_assistententreffen': schicht.ist_assistententreffen,
                                'ist_kurzfristig': schicht.ist_kurzfristig,
                                'ist_ausfallgeld': schicht.ist_ausfallgeld,
                                'ist_pcg': schicht.ist_pcg,
                                'ist_schulung': schicht.ist_schulung,
                                'beginn_adresse': schicht.beginn_andere_adresse,
                                'ende_adresse': schicht.ende_andere_adresse
                                })
            else:
                ausgabe.append({'beginn': rest['start'],
                                'ende': rest['ende'],
                                'asn': schicht.asn,
                                'assistent': schicht.assistent,
                                'schicht_id': schicht.id,
                                'ist_assistententreffen': schicht.ist_assistententreffen,
                                'ist_kurzfristig': schicht.ist_kurzfristig,
                                'ist_ausfallgeld': schicht.ist_ausfallgeld,
                                'ist_pcg': schicht.ist_pcg,
                                'ist_schulung': schicht.ist_schulung,
                                'beginn_adresse': schicht.beginn_andere_adresse,
                                'ende_adresse': schicht.ende_andere_adresse
                                })

            rest['start'] = neuer_start_rest
    else:
        # ausgabe.append(schicht)
        ausgabe.append({
            'beginn': schicht.beginn,
            'ende': schicht.ende,
            'asn': schicht.asn,
            'assistent': schicht.assistent,
            'schicht_id': schicht.id,
            'ist_assistententreffen': schicht.ist_assistententreffen,
            'ist_kurzfristig': schicht.ist_kurzfristig,
            'ist_ausfallgeld': schicht.ist_ausfallgeld,
            'ist_pcg': schicht.ist_pcg,
            'ist_schulung': schicht.ist_schulung,
            'beginn_adresse': schicht.beginn_andere_adresse,
            'ende_adresse': schicht.ende_andere_adresse
        })

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
    return get_duration(schicht['beginn'], schicht['ende'], "minutes") / 60


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


def get_lohn(assistent, datum, session):
    erfahrungsstufe = get_erfahrungsstufe(assistent=assistent, datum=datum)
    for lohn in session.query(Lohn).filter(
            Lohn.erfahrungsstufe == erfahrungsstufe).filter(
        Lohn.gueltig_ab < datum).filter(
        Lohn.eingruppierung == 5
    ).order_by(desc(Lohn.gueltig_ab)).limit(1):
        return lohn
    return False


def get_sliced_schichten(start, end, session):
    sliced_schichten = []
    for schicht in session.query(Schicht).filter(
            or_(
                Schicht.beginn.between(start, end),
                Schicht.ende.between(start, end)
            )
    ):
        sliced_schichten += split_by_null_uhr(schicht)

    return sliced_schichten


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

    return datetime(year=jahr, month=3 + m, day=tmp)


def check_feiertag(datum):
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
    ostersonntag = berechne_ostern(jahr)
    karfreitag = ostersonntag - timedelta(days=2)
    feiertag = {'name': 'Karfreitag', 'd': int(karfreitag.strftime('%d')),
                'm': int(karfreitag.strftime('%m')), 'Y': 0}
    feiertage.append(feiertag)
    ostermontag = ostersonntag + timedelta(days=1)
    feiertag = {'name': 'Ostermontag', 'd': int(ostermontag.strftime('%d')),
                'm': int(ostermontag.strftime('%m')), 'Y': 0}
    feiertage.append(feiertag)
    himmelfahrt = ostersonntag + timedelta(days=40)
    feiertag = {'name': 'Christi Himmelfahrt', 'd': int(himmelfahrt.strftime('%d')),
                'm': int(himmelfahrt.strftime('%m')), 'Y': 0}
    feiertage.append(feiertag)
    pfingstsonntag = ostersonntag + timedelta(days=49)
    feiertag = {'name': 'Pfingstsonntag', 'd': int(pfingstsonntag.strftime('%d')),
                'm': int(pfingstsonntag.strftime('%m')), 'Y': 0}
    feiertage.append(feiertag)
    pfingstmontag = ostersonntag + timedelta(days=50)
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


def berechne_sa_so_weisil_feiertagszuschlaege(schicht: Schicht):
    feiertagsstunden = 0
    feiertagsstunden_steuerfrei = 0
    feiertagsstunden_steuerpflichtig = 0
    feiertagsarray = {}
    zuschlagsgrund = ''

    anfang = schicht['beginn']
    ende = schicht['ende']

    if check_feiertag(anfang) != '':
        feiertagsstunden = berechne_stunden(schicht=schicht)

        feiertagsarray = {'zuschlagsgrund': 'Feiertag',
                          'stunden_gesamt': feiertagsstunden,
                          'stunden_steuerfrei': feiertagsstunden,
                          'stunden_steuerpflichtig': 0,
                          'add_info': check_feiertag(anfang)
                          }
    elif datetime(year=anfang.year, month=anfang.month, day=anfang.day) == \
            datetime(anfang.year, 12, 24) or \
            datetime(anfang.year, anfang.month, anfang.day) == \
            datetime(anfang.year, 12, 31):
        if datetime(anfang.year, anfang.month, anfang.day) == \
                datetime(anfang.year, 12, 24):
            zuschlagsgrund = 'Hl. Abend'
        if datetime(anfang.year, anfang.month, anfang.day) == \
                datetime(anfang.year, 12, 31):
            zuschlagsgrund = 'Silvester'

        sechsuhr = datetime(anfang.year, anfang.month, anfang.day, 6, 0, 0)
        vierzehn_uhr = datetime(anfang.year, anfang.month, anfang.day, 14, 0, 0)

        if anfang < sechsuhr:
            if ende <= sechsuhr:
                feiertagsstunden_steuerfrei = feiertagsstunden_steuerpflichtig = 0
            elif sechsuhr < ende <= vierzehn_uhr:
                feiertagsstunden_steuerpflichtig = get_duration(ende, sechsuhr, 'hours')
                feiertagsstunden_steuerfrei = 0
            elif vierzehn_uhr < ende:
                feiertagsstunden_steuerpflichtig = 8
                feiertagsstunden_steuerfrei = get_duration(vierzehn_uhr, ende, 'hours')
        elif sechsuhr <= anfang:
            if ende <= vierzehn_uhr:
                feiertagsstunden_steuerpflichtig = get_duration(ende, anfang, 'hours')
                feiertagsstunden_steuerfrei = 0
            elif vierzehn_uhr < ende:
                feiertagsstunden_steuerpflichtig = get_duration(anfang, vierzehn_uhr, 'hours')
                feiertagsstunden_steuerfrei = get_duration(vierzehn_uhr, ende, 'hours')

        feiertagsstunden = feiertagsstunden_steuerfrei + feiertagsstunden_steuerpflichtig
        feiertagsarray = {'zuschlagsgrund': zuschlagsgrund,
                          'stunden_gesamt': feiertagsstunden,
                          'stunden_steuerfrei': feiertagsstunden_steuerfrei,
                          'stunden_steuerpflichtig': feiertagsstunden_steuerpflichtig,
                          'add_info': '13:00 - 21:00 Uhr'
                          }
    elif anfang.weekday() == 6:
        feiertagsstunden = berechne_stunden(schicht=schicht)
        feiertagsarray = {'zuschlagsgrund': 'Sonntag',
                          'stunden_gesamt': feiertagsstunden,
                          'stunden_steuerfrei': feiertagsstunden,
                          'stunden_steuerpflichtig': 0,
                          'add_info': ''
                          }
    elif anfang.weekday() == 5:
        dreizehn_uhr = datetime(anfang.year, anfang.month, anfang.day, 13, 0, 0)
        einundzwanzig_uhr = datetime(anfang.year, anfang.month, anfang.day, 21, 0, 0)

        if anfang < dreizehn_uhr:
            if ende < dreizehn_uhr:
                feiertagsstunden = 0
            elif dreizehn_uhr < ende <= einundzwanzig_uhr:
                feiertagsstunden = get_duration(dreizehn_uhr, ende, 'hours')
            else:  # ende > einundzwanzig_uhr:
                feiertagsstunden = 8  # 21 - 13
        elif dreizehn_uhr <= anfang < einundzwanzig_uhr:
            if ende < einundzwanzig_uhr:
                feiertagsstunden = berechne_stunden(schicht=schicht)
            elif ende > einundzwanzig_uhr:
                feiertagsstunden = get_duration(anfang, einundzwanzig_uhr, 'hours')
        else:
            feiertagsstunden = 0

        feiertagsarray = {'zuschlagsgrund': 'Samstag',
                          'stunden_gesamt': feiertagsstunden,
                          'stunden_steuerfrei': 0,
                          'stunden_steuerpflichtig': feiertagsstunden,
                          'add_info': '13:00 - 21:00 Uhr'
                          }

    return feiertagsarray


def get_nachtstunden(schicht):
    """Gibt die Anzahl der Stunden einer Schicht zurück, die vor 6 Uhr und nach 21 Uhr stattfinden"""

    nachtstunden = 0

    beginn_jahr = int(schicht['beginn'].strftime('%Y'))
    beginn_monat = int(schicht['beginn'].strftime('%m'))
    beginn_tag = int(schicht['beginn'].strftime('%d'))

    null_uhr = datetime(beginn_jahr, beginn_monat, beginn_tag, 0, 0, 0)
    sechs_uhr = datetime(beginn_jahr, beginn_monat, beginn_tag, 6, 0, 0)
    einundzwanzig_uhr = datetime(beginn_jahr, beginn_monat, beginn_tag, 21, 0, 0)

    # schicht beginnt zwischen 0 und 6 uhr
    if null_uhr <= schicht['beginn'] <= sechs_uhr:
        if schicht['ende'] <= sechs_uhr:
            # schicht endet spätestens 6 uhr
            nachtstunden += get_duration(schicht['beginn'], schicht['ende'], 'minutes') / 60

        elif sechs_uhr <= schicht['ende'] <= einundzwanzig_uhr:
            # schicht endet nach 6 uhr aber vor 21 uhr
            nachtstunden += get_duration(schicht['beginn'], sechs_uhr, 'minutes') / 60

        else:
            # schicht beginnt vor 6 uhr und geht über 21 Uhr hinaus
            # das bedeutet ich ziehe von der kompletten schicht einfach die 15 Stunden Tagschicht ab.
            # es bleibt der Nacht-An
            nachtstunden += get_duration(schicht['beginn'], schicht['ende'], 'minutes') / 60 - 15
    # schicht beginnt zwischen 6 und 21 uhr
    elif sechs_uhr <= schicht['beginn'] <= einundzwanzig_uhr:
        # fängt am tag an, geht aber bis in die nachtstunden
        if schicht['ende'] > einundzwanzig_uhr:
            nachtstunden += get_duration(einundzwanzig_uhr, schicht['ende'], 'minutes') / 60
    else:
        # schicht beginnt nach 21 uhr - die komplette schicht ist in der nacht
        nachtstunden += get_duration(schicht['beginn'], schicht['ende'], 'minutes') / 60

    return nachtstunden


def sort_schicht_data_by_beginn(schichten: list):
    """sortiert die schichten an einem tag (in Form einer Liste von dicts von strings)
    nach ihrem beginn"""
    ausgabe = []

    for schicht in schichten:
        insert_flag = False
        beginn_akt_schicht = strptime(schicht['von'], "%H:%M")
        for zaehler in range(0, len(ausgabe)):
            if beginn_akt_schicht < strptime(ausgabe[zaehler]['von'], "%H:%M"):
                ausgabe.insert(zaehler, schicht)
                insert_flag = True
                break
        if not insert_flag:
            ausgabe.append(schicht)

    return ausgabe


def berechne_urlaub_au_saetze(datum, session, assistent):
    akt_monat = datetime(year=datum.year, month=datum.month, day=1)
    for zaehler in range(1, 7):
        vormonat_letzter = akt_monat - timedelta(days=1)
        akt_monat = datetime(year=vormonat_letzter.year, month=vormonat_letzter.month, day=1)
    startmonat = akt_monat

    bruttosumme = 0
    stundensumme = 0
    zaehler = 0
    for brutto in session.query(Brutto).filter(
            Brutto.monat.between(
                startmonat,
                datetime(year=datum.year, month=datum.month, day=1)
            )
    ).filter(Brutto.as_id == assistent.id):
        bruttosumme += brutto.bruttolohn
        stundensumme += brutto.stunden_gesamt
        zaehler += 1
    if zaehler == 0 or stundensumme == 0:
        return {
            'stunden_pro_tag': 1,
            'pro_stunde': 5
        }

    return {
        'stunden_pro_tag': (stundensumme / zaehler) / 30,
        'pro_stunde': bruttosumme / stundensumme
    }


def get_ersten_xxtag(int_weekday, erster=datetime.now()):
    for counter in range(1, 8):
        if datetime(year=erster.year, month=erster.month, day=counter, hour=0,
                    minute=0).weekday() == int_weekday:
            return counter


def check_au(datum, session):
    if session.query(AU.id).filter(
            AU.beginn <= datum).filter(AU.ende >= datum).with_entities(func.count()).scalar():
        return True
    else:
        return False


def check_urlaub(datum, session):
    if session.query(Urlaub.id).filter(
            Urlaub.beginn <= datum).filter(Urlaub.ende >= datum).with_entities(func.count()).scalar():
        return True
    else:
        return False
