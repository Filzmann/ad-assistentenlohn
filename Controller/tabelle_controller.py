from datetime import datetime, timedelta

from sqlalchemy import or_, desc
from sqlalchemy.future import select

from Model.assistent import Assistent
from Model.lohn import Lohn
from Model.schicht import Schicht
from View.tabelle_view import TabelleView
from Helpers.help_functions import *


class TabelleController:
    def __init__(self, parent_controller, session, parent_view, assistent):
        self.assistent = assistent
        self.session = session
        self.parent_view = parent_view
        # initialisierung
        self.start = datetime(year=datetime.now().year,
                              month=datetime.now().month,
                              day=1)
        self.end = verschiebe_monate(offset=1, datum=self.start)
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
        self.end = verschiebe_monate(offset=1, datum=self.start)
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

            nachtstunden = get_nachtstunden(schicht)

            # zuschläge
            zuschlaege = berechne_sa_so_weisil_feiertagszuschlaege(schicht)
            if zuschlaege:
                grund = zuschlaege['zuschlagsgrund']
                # Grund zu lower-case mit "_" statt " " und ohn punkte, damit es dem Spaltennamen der Tabelle entspricht
                spaltenname = grund.lower().replace('.', '').replace(' ', '_') + '_zuschlag'
                stundenzuschlag = getattr(lohn, spaltenname)
                schichtzuschlag = zuschlaege['stunden_gesamt'] * stundenzuschlag
                zuschlaege_text = grund + ': ' \
                                  + "{:,.2f}".format(zuschlaege['stunden_gesamt']) \
                                  + ' Std = ' \
                                  + "{:,.2f}€".format(schichtzuschlag)
            else:
                zuschlaege_text = ''

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
                    'zuschlaege': zuschlaege_text
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

    def get_lohn(self, assistent, datum):
        erfahrungsstufe = get_erfahrungsstufe(assistent=assistent, datum=datum)
        for lohn in self.session.query(Lohn).filter(
                Lohn.erfahrungsstufe == erfahrungsstufe).filter(
            Lohn.gueltig_ab < datum).filter(
            Lohn.eingruppierung == 5
        ).order_by(desc(Lohn.gueltig_ab)).limit(1):
            return lohn
        return False
