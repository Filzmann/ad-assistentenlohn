from sqlalchemy import or_
from Helpers.help_functions import *
from Model.arbeitsunfaehigkeit import AU
from Model.brutto import Brutto
from Model.urlaub import Urlaub
from View.summen_view import SummenView


def check_schicht(datum: datetime, session):
    """prüft, ob an einem gegeben Datum eine Schicht ist."""
    tagbeginn = datetime(year=datum.year, month=datum.month, day=datum.day, hour=0, minute=0, second=0)
    tagende = datetime(year=datum.year, month=datum.month, day=datum.day, hour=23, minute=59, second=59)

    for schicht in session.query(Schicht.id).filter(
        or_(
            or_(
                Schicht.beginn.between(tagbeginn, tagende),
                Schicht.ende.between(tagbeginn, tagende)
            ),
            and_(
                tagbeginn < Schicht.beginn,
                tagende > Schicht.ende
            )
        )
    ):
        return True
    return False


def get_freie_sonntage(year, session):
    # erster sonntag
    janfirst = datetime(year, 1, 1)
    sunday = (7 - janfirst.weekday()) % 7
    sunday = datetime(year=year, month=1, day=sunday)

    wochencounter = 0
    sontagsschichtcounter = 0
    for kw in range(1, 54):
        if sunday.year == year:
            wochencounter += 1
            if check_schicht(sunday, session):
                sontagsschichtcounter += 1
        sunday = sunday + timedelta(days=7)
    return wochencounter - sontagsschichtcounter


class SummenController:
    def __init__(self, session, parent_view, assistent):
        self.assistent = assistent
        self.session = session
        self.parent_view = parent_view
        # initialisierung
        self.start = datetime(year=datetime.now().year,
                              month=datetime.now().month,
                              day=1)
        self.end = verschiebe_monate(offset=1, datum=self.start)

        data = self.calculate()
        self.view = SummenView(parent_view=parent_view,
                               data=data)

    def change_arbeitsdatum(self, datum, session):
        self.start = datetime(year=datum.year,
                              month=datum.month,
                              day=1)
        self.end = verschiebe_monate(offset=1, datum=self.start)
        data = self.calculate(session=session)
        self.view.draw(data=data)

    def calculate(self, session=None):
        if not session:
            session = self.session

        schichten = get_sliced_schichten(start=self.start, end=self.end, session=session)
        freie_sonntage = get_freie_sonntage(self.start.year, session=self.session)

        schichten_view_data = {
            'arbeitsstunden': 0,
            'stundenlohn': 0,
            'lohn': 0,
            'nachtstunden': 0,
            'nachtzuschlag': 0,
            'nachtzuschlag_kumuliert': 0,
            'bsd': 0,
            'bsd_stunden': 0,
            'bsd_kumuliert': 0,
            'wegegeld_bsd': 0,
            'orga_zuschlag': 0,
            'orga_zuschlag_kumuliert': 0,
            'wechselschicht_zuschlag': 0,
            'wechselschicht_zuschlag_kumuliert': 0,
            'freizeitausgleich': 0,
            'bruttolohn': 0,
            'anzahl_feiertage': 0,
            'freie_sonntage': str(freie_sonntage),
            'moegliche_arbeitssonntage': str(freie_sonntage - 15),
            'urlaubsstunden': 0,
            'stundenlohn_urlaub': 0,
            'urlaubslohn': 0,
            'austunden': 0,
            'stundenlohn_au': 0,
            'aulohn': 0

        }
        for schicht in schichten:

            #     if not schicht['beginn'].strftime('%d') in schichten_view_data.keys():
            #         schichten_view_data[schicht['beginn'].strftime('%d')] = []

            # stunden
            stunden = berechne_stunden(schicht)
            schichten_view_data['arbeitsstunden'] += stunden

            lohn = get_lohn(session=self.session, assistent=self.assistent, datum=schicht['beginn'])
            schichten_view_data['stundenlohn'] = lohn.grundlohn
            schichten_view_data['lohn'] += stunden * lohn.grundlohn
            schichten_view_data['bruttolohn'] += stunden * lohn.grundlohn

            # nacht
            nachtstunden = get_nachtstunden(schicht)
            schichten_view_data['nachtstunden'] += nachtstunden
            schichten_view_data['nachtzuschlag'] = lohn.nacht_zuschlag
            schichten_view_data['nachtzuschlag_kumuliert'] += lohn.nacht_zuschlag * nachtstunden
            schichten_view_data['bruttolohn'] += lohn.nacht_zuschlag * nachtstunden

            # bsd
            schichten_view_data['bsd_stunden'] += stunden if schicht['ist_kurzfristig'] else 0
            schichten_view_data['bsd'] += (lohn.grundlohn * 0.2) if schicht['ist_kurzfristig'] else 0
            schichten_view_data['bsd_kumuliert'] += (lohn.grundlohn * stunden * 0.2) if schicht[
                'ist_kurzfristig'] else 0
            schichten_view_data['bruttolohn'] += (lohn.grundlohn * stunden * 0.2) if schicht['ist_kurzfristig'] else 0
            # todo wegegeld

            # orga
            schichten_view_data['orga_zuschlag'] = lohn.orga_zuschlag
            schichten_view_data['orga_zuschlag_kumuliert'] += lohn.orga_zuschlag * stunden
            schichten_view_data['bruttolohn'] += lohn.orga_zuschlag * stunden

            # wechsel
            schichten_view_data['wechselschicht_zuschlag'] = lohn.wechselschicht_zuschlag
            schichten_view_data['wechselschicht_zuschlag_kumuliert'] += lohn.wechselschicht_zuschlag * stunden
            schichten_view_data['bruttolohn'] += lohn.wechselschicht_zuschlag * stunden

            # zuschläge
            zuschlaege = berechne_sa_so_weisil_feiertagszuschlaege(schicht)
            if zuschlaege:
                grund = zuschlaege['zuschlagsgrund']
                # Grund zu lower-case mit "_" statt " " und ohn punkte, damit es dem Spaltennamen der Tabelle entspricht
                spaltenname = grund.lower().replace('.', '').replace(' ', '_') + '_zuschlag'

                stundenzuschlag = getattr(lohn, spaltenname)
                schichtzuschlag = zuschlaege['stunden_gesamt'] * stundenzuschlag

                if spaltenname + "_bezeichner" in schichten_view_data.keys():
                    schichten_view_data[spaltenname + "_stunden"] += zuschlaege['stunden_gesamt']
                    schichten_view_data[spaltenname + "_kumuliert"] += schichtzuschlag
                else:
                    schichten_view_data[spaltenname + "_bezeichner"] = grund
                    schichten_view_data[spaltenname + "_stunden"] = zuschlaege['stunden_gesamt']
                    schichten_view_data[spaltenname + "_pro_stunde"] = stundenzuschlag
                    schichten_view_data[spaltenname + "_kumuliert"] = schichtzuschlag

                schichten_view_data['bruttolohn'] += schichtzuschlag

        # Urlaube ermitteln
        # Todo urlaube, die länger als ein Monat sind und in diesem Monat weder starten noch enden
        for urlaub in self.session.query(Urlaub).filter(
                or_(
                    Urlaub.beginn.between(self.start, self.end),
                    Urlaub.ende.between(self.start, self.end)
                )).filter(self.start != Urlaub.ende).filter(self.end != Urlaub.beginn):

            erster_tag = urlaub.beginn.day if urlaub.beginn > self.start else self.start.day
            letzter_tag = urlaub.ende.day if urlaub.ende < self.end else (self.end - timedelta(days=1)).day

            urlaubsstunden = berechne_urlaub_au_saetze(datum=self.start,
                                                       assistent=self.assistent,
                                                       session=self.session)['stunden_pro_tag']
            urlaubslohn = berechne_urlaub_au_saetze(datum=self.start,
                                                    assistent=self.assistent,
                                                    session=self.session)['pro_stunde']

            for tag in range(erster_tag, letzter_tag + 1):
                schichten_view_data['urlaubsstunden'] += urlaubsstunden
                schichten_view_data['stundenlohn_urlaub'] = urlaubslohn
                schichten_view_data['urlaubslohn'] += urlaubsstunden * urlaubslohn
                schichten_view_data['bruttolohn'] += urlaubsstunden * urlaubslohn

        # AU ermitteln
        # Todo AU, die länger als ein Monat sind und in diesem Monat weder starten noch enden
        for au in self.session.query(AU).filter(
                or_(
                    AU.beginn.between(self.start, self.end),
                    AU.ende.between(self.start, self.end)
                )).filter(self.start != AU.ende).filter(self.end != AU.beginn):

            erster_tag = au.beginn.day if au.beginn > self.start else self.start.day
            letzter_tag = au.ende.day if au.ende < self.end else (self.end - timedelta(days=1)).day

            austunden = berechne_urlaub_au_saetze(datum=self.start,
                                                  assistent=self.assistent,
                                                  session=self.session)['stunden_pro_tag']
            aulohn = berechne_urlaub_au_saetze(datum=self.start,
                                               assistent=self.assistent,
                                               session=self.session)['pro_stunde']

            for tag in range(erster_tag, letzter_tag + 1):
                schichten_view_data['austunden'] += austunden
                schichten_view_data['stundenlohn_au'] = aulohn
                schichten_view_data['aulohn'] += austunden * aulohn
                schichten_view_data['bruttolohn'] += austunden * aulohn

        # Freizeitausgleich
        # anzahl aller feiertage ermitteln
        letzter_tag = (self.end - timedelta(seconds=1)).day
        ausgleichsstunden = berechne_urlaub_au_saetze(datum=self.start,
                                                      assistent=self.assistent,
                                                      session=self.session)['stunden_pro_tag']
        ausgleichslohn = berechne_urlaub_au_saetze(datum=self.start,
                                                   assistent=self.assistent,
                                                   session=self.session)['pro_stunde']
        for tag in range(1, letzter_tag + 1):
            if check_feiertag(datetime(year=self.start.year, month=self.start.month, day=tag)):
                schichten_view_data['anzahl_feiertage'] += 1
                schichten_view_data['freizeitausgleich'] += ausgleichslohn * ausgleichsstunden

        ueberstunden = schichten_view_data['arbeitsstunden'] \
                       + schichten_view_data['urlaubsstunden'] \
                       + schichten_view_data['austunden'] \
                       - 168.5
        if ueberstunden > 0:
            schichten_view_data['ueberstunden'] = ueberstunden
            schichten_view_data['ueberstunden_pro_stunde'] = lohn.ueberstunden_zuschlag
            schichten_view_data['ueberstunden_kumuliert'] = lohn.ueberstunden_zuschlag * ueberstunden
            schichten_view_data['bruttolohn'] += lohn.ueberstunden_zuschlag * ueberstunden

        self.save_brutto(data=schichten_view_data)

        return schichten_view_data

    def save_brutto(self, data):
        check_result = self.session.query(Brutto.id).filter(
            Brutto.monat == self.start).filter(
            Brutto.as_id == self.assistent.id).count()
        if check_result:
            # Update
            for brutto in self.session.query(Brutto).filter(
                    Brutto.monat == self.start).filter(Brutto.as_id == self.assistent.id):
                brutto.bruttolohn = data['bruttolohn']
                brutto.stunden_gesamt = data['arbeitsstunden']  # + data['urlaubsstunden'] + data['austunden']

        else:
            # Create
            brutto = Brutto(monat=self.start,
                            as_id=self.assistent.id,
                            bruttolohn=data['bruttolohn'],
                            stunden_gesamt=data['arbeitsstunden'])
            self.session.add(brutto)
        self.session.commit()
