from sqlalchemy import or_, desc

from Helpers.help_functions import *
from Model.lohn import Lohn
from View.summen_view import SummenView


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

        # aufräumen falls noch "Teilschichten" in der Session rumliegen
        for schicht in self.session.query(Schicht).filter(Schicht.original_id):
            self.session.delete(schicht)
            self.session.commit()

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

        schichten = self.get_sliced_schichten(start=self.start, end=self.end, session=session)
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
            # Todo wegegeld
            'wegegeld_bsd': 0,
            'orga_zuschlag': 0,
            'orga_zuschlag_kumuliert': 0,
            'wechselschicht_zuschlag': 0,
            'wechselschicht_zuschlag_kumuliert': 0,
            # todo freizeitausgleich
            'freizeitausgleich': 0,
            'bruttolohn': 0
            # todo freie Sonntage

        }
        for schicht in schichten:
            if not schicht['beginn'].strftime('%d') in schichten_view_data.keys():
                schichten_view_data[schicht['beginn'].strftime('%d')] = []

            # stunden
            stunden = berechne_stunden(schicht)
            schichten_view_data['arbeitsstunden'] += stunden

            lohn = self.get_lohn(assistent=self.assistent, datum=schicht['beginn'])
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

                if spaltenname in schichten_view_data.keys():

                    if spaltenname + "_bezeichner" in schichten_view_data.keys():
                        schichten_view_data[spaltenname + "_stunden"] += zuschlaege['stunden_gesamt']
                        schichten_view_data[spaltenname + "_kumuliert"] += schichtzuschlag
                    else:
                        schichten_view_data[spaltenname + "_bezeichner"] = grund
                        schichten_view_data[spaltenname + "_stunden"] = zuschlaege['stunden_gesamt']
                        schichten_view_data[spaltenname + "_pro_stunde"] = stundenzuschlag
                        schichten_view_data[spaltenname + "_kumuliert"] = schichtzuschlag

        return schichten_view_data

    def get_sliced_schichten(self, start, end, session=None):
        sliced_schichten = []
        if session:
            self.session = session

        for schicht in self.session.query(Schicht).filter(
                or_(
                    Schicht.beginn.between(start, end),
                    Schicht.ende.between(start, end)
                )
        ):
            sliced_schichten += split_by_null_uhr(schicht)

        return sliced_schichten

        # TODO Urlaub und AU auch hier splitten

    def get_lohn(self, assistent, datum):
        erfahrungsstufe = get_erfahrungsstufe(assistent=assistent, datum=datum)
        for lohn in self.session.query(Lohn).filter(
                Lohn.erfahrungsstufe == erfahrungsstufe).filter(
            Lohn.gueltig_ab < datum).filter(
            Lohn.eingruppierung == 5
        ).order_by(desc(Lohn.gueltig_ab)).limit(1):
            return lohn
        return False
