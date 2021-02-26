from Controller.arbeitsunfaehigkeit_controller import AUController
from Controller.schicht_controller import SchichtController
from Controller.urlaub_controller import UrlaubController
from Helpers.help_functions import *
from Model.arbeitsunfaehigkeit import AU
from Model.urlaub import Urlaub
from View.tabelle_view import TabelleView


class TabelleController:
    def __init__(self, session, parent_view, assistent, root_window_controller):
        self.assistent = assistent
        self.session = session
        self.parent_view = parent_view
        self.nav_panel = None
        self.root_window_controller = root_window_controller
        # initialisierung
        self.start = datetime(year=datetime.now().year,
                              month=datetime.now().month,
                              day=1)
        self.end = verschiebe_monate(offset=1, datum=self.start)
        letzter_tag = (self.end - timedelta(seconds=1)).day

        data = self.calculate()
        self.view = TabelleView(parent_view=parent_view,
                                parent_controller=self,
                                data=data,
                                anzahl_tage=letzter_tag,
                                start=self.start)

    def change_arbeitsdatum(self, datum, session):
        self.start = datetime(year=datum.year,
                              month=datum.month,
                              day=1)
        self.end = verschiebe_monate(offset=1, datum=self.start)
        data = self.calculate(session)

        letzter_tag = (self.end - timedelta(seconds=1)).day
        self.view.draw(data=data,
                       anzahl_tage=letzter_tag,
                       start=self.start)

    def calculate(self, session=None):
        if session:
            self.session = session
        schichten = get_sliced_schichten(start=self.start, end=self.end, session=self.session)

        if not schichten:
            self.add_feste_schichten(self.start, self.end)
            schichten = get_sliced_schichten(start=self.start, end=self.end, session=session)

        schichten_view_data = {}
        for schicht in schichten:
            if not schicht['beginn'].strftime('%d') in schichten_view_data.keys():
                schichten_view_data[schicht['beginn'].strftime('%d')] = []

            # at etc
            asn_add = ''
            asn_add += 'AT ' if schicht['ist_assistententreffen'] else ''
            asn_add += 'PCG ' if schicht['ist_pcg'] else ''
            asn_add += 'RB/BSD ' if schicht['ist_kurzfristig'] else ''
            asn_add += 'AFG ' if schicht['ist_ausfallgeld'] else ''

            # stunden
            stunden = berechne_stunden(schicht)

            lohn = get_lohn(session=self.session, assistent=self.assistent, datum=schicht['beginn'])

            nachtstunden = get_nachtstunden(schicht)

            # zuschläge
            zuschlaege = berechne_sa_so_weisil_feiertagszuschlaege(schicht)
            zuschlaege_text = ''
            if zuschlaege:
                if zuschlaege['stunden_gesamt'] > 0:
                    grund = zuschlaege['zuschlagsgrund']
                    # Grund zu lower-case mit "_" statt " " und ohne punkte,
                    # damit es dem Spaltennamen der Tabelle entspricht
                    spaltenname = grund.lower().replace('.', '').replace(' ', '_') + '_zuschlag'
                    stundenzuschlag = getattr(lohn, spaltenname)
                    schichtzuschlag = zuschlaege['stunden_gesamt'] * stundenzuschlag
                    zuschlaege_text = grund \
                                      + ': ' \
                                      + "{:,.2f}".format(zuschlaege['stunden_gesamt']) \
                                      + ' Std = ' \
                                      + "{:,.2f}€".format(schichtzuschlag)

            schicht_id = schicht['schicht_id']
            schichten_view_data[schicht['beginn'].strftime('%d')].append(
                {
                    'schicht_id': schicht_id,
                    'von': schicht['beginn'].strftime('%H:%M'),
                    'bis': schicht['ende'].strftime('%H:%M'),
                    'asn': asn_add + schicht['asn'].kuerzel,
                    'stunden': "{:,.2f}".format(stunden),
                    'stundenlohn': "{:,.2f}€".format(lohn.grundlohn),
                    'schichtlohn': "{:,.2f}€".format(lohn.grundlohn * stunden),
                    'bsd': "{:,.2f}€".format(lohn.grundlohn * stunden * 0.2) if schicht['ist_kurzfristig'] else ' ',
                    'orgazulage': "{:,.2f}€".format(lohn.orga_zuschlag),
                    'orgazulage_schicht': "{:,.2f}€".format(lohn.orga_zuschlag * stunden),
                    'wechselzulage': "{:,.2f}€".format(lohn.wechselschicht_zuschlag),
                    'wechselzulage_schicht': "{:,.2f}€".format(lohn.wechselschicht_zuschlag * stunden),
                    'nachtstunden': "{:,.2f}".format(nachtstunden) if nachtstunden > 0 else ' ',
                    'nachtzuschlag': "{:,.2f}€".format(lohn.nacht_zuschlag),
                    'nachtzuschlag_schicht': "{:,.2f}€".format(
                        lohn.nacht_zuschlag * nachtstunden) if nachtstunden > 0 else ' ',
                    'zuschlaege': zuschlaege_text,
                    'type': 'schicht'
                }
            )

        # mehrere Schichten an jedem Tag nach schichtbeginn sortieren
        for key in schichten_view_data:
            schichten_view_data[key] = sort_schicht_data_by_beginn(schichten_view_data[key])

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
                if tag not in schichten_view_data.keys():
                    schichten_view_data["{:02d}".format(tag)] = []
                schichten_view_data["{:02d}".format(tag)].append(
                    {
                        'schicht_id': urlaub.id,
                        'von': ' ',
                        'bis': ' ',
                        'asn': 'Urlaub',
                        'stunden': "{:,.2f}".format(urlaubsstunden),
                        'stundenlohn': "{:,.2f}€".format(urlaubslohn),
                        'schichtlohn': "{:,.2f}€".format(urlaubslohn * urlaubsstunden),
                        'bsd': ' ',
                        'orgazulage': ' ',
                        'orgazulage_schicht': ' ',
                        'wechselzulage': ' ',
                        'wechselzulage_schicht': ' ',
                        'nachtstunden': ' ',
                        'nachtzuschlag': ' ',
                        'nachtzuschlag_schicht': ' ',
                        'zuschlaege': ' ',
                        'type': 'urlaub'
                    }
                )

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
                if tag not in schichten_view_data.keys():
                    schichten_view_data["{:02d}".format(tag)] = []
                schichten_view_data["{:02d}".format(tag)].append(
                    {
                        'schicht_id': au.id,
                        'von': ' ',
                        'bis': ' ',
                        'asn': 'AU/krank',
                        'stunden': "{:,.2f}".format(austunden),
                        'stundenlohn': "{:,.2f}€".format(aulohn),
                        'schichtlohn': "{:,.2f}€".format(aulohn * austunden),
                        'bsd': ' ',
                        'orgazulage': ' ',
                        'orgazulage_schicht': ' ',
                        'wechselzulage': ' ',
                        'wechselzulage_schicht': ' ',
                        'nachtstunden': ' ',
                        'nachtzuschlag': ' ',
                        'nachtzuschlag_schicht': ' ',
                        'zuschlaege': ' ',
                        'type': 'au'
                    }
                )

        return schichten_view_data

    def kill_schicht(self, schicht_id, typ='schicht'):
        if typ == "schicht":
            for schicht in self.session.query(Schicht).filter(Schicht.id == schicht_id):
                self.session.delete(schicht)
                self.session.commit()
                self.change_arbeitsdatum(schicht.beginn, session=self.session)
        elif typ == "urlaub":
            for u in self.session.query(Urlaub).filter(Urlaub.id == schicht_id):
                self.session.delete(u)
                self.session.commit()
                self.change_arbeitsdatum(u.beginn, session=self.session)
        elif typ == "au":
            for au in self.session.query(AU).filter(AU.id == schicht_id):
                self.session.delete(au)
                self.session.commit()
                self.change_arbeitsdatum(au.beginn, session=self.session)
        else:
            pass

    def edit_schicht(self, schicht_id, typ='schicht'):
        """

        :param schicht_id:
        :param typ:
        :return:
        """

        if typ == 'schicht':
            for schicht in self.session.query(Schicht).filter(Schicht.id == schicht_id):
                SchichtController(parent_controller=self.root_window_controller,
                                  session=self.session,
                                  assistent=schicht.assistent,
                                  asn=schicht.asn,
                                  edit_schicht=schicht,
                                  datum=schicht.beginn,
                                  nav_panel=self.nav_panel)
        elif typ == 'urlaub':
            for u in self.session.query(Urlaub).filter(Urlaub.id == schicht_id):
                UrlaubController(
                    parent_controller=self.root_window_controller,
                    session=self.session,
                    assistent=u.assistent,
                    urlaub=u,
                    nav_panel=self.nav_panel
                )
        elif typ == 'au':
            for au in self.session.query(AU).filter(AU.id == schicht_id):
                AUController(
                    parent_controller=self.root_window_controller,
                    session=self.session,
                    assistent=au.assistent,
                    au=au,
                    nav_panel=self.nav_panel
                )
        else:
            pass

    def new_schicht(self, datum):
        SchichtController(parent_controller=self.root_window_controller,
                          session=self.session,
                          assistent=self.assistent,
                          datum=datum,
                          nav_panel=self.nav_panel)

    def add_feste_schichten(self, erster_tag, letzter_tag):
        wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        for feste_schicht in self.assistent.feste_schichten:
            wtag_int = wochentage.index(feste_schicht.wochentag)
            erster_xxtag_des_monats = get_ersten_xxtag(wtag_int, erster_tag)
            monat = erster_tag.month
            year = erster_tag.year
            maxday = (letzter_tag - timedelta(days=1)).day
            asn = feste_schicht.asn
            for woche in range(0, 5):
                tag = woche * 7 + erster_xxtag_des_monats
                if tag <= maxday:
                    if feste_schicht.beginn < feste_schicht.ende:
                        start = datetime(year=year,
                                         month=monat,
                                         day=tag,
                                         hour=feste_schicht.beginn.hour,
                                         minute=feste_schicht.beginn.minute)
                        end = datetime(year=year,
                                       month=monat,
                                       day=tag,
                                       hour=feste_schicht.ende.hour,
                                       minute=feste_schicht.ende.minute)
                    # nachtschicht. es gibt keine regelmäßigen dienstreisen!
                    else:
                        start = datetime(year=year,
                                         month=monat,
                                         day=tag,
                                         hour=feste_schicht.beginn.hour,
                                         minute=feste_schicht.beginn.minute)
                        end = datetime(year=year,
                                       month=monat,
                                       day=tag,
                                       hour=feste_schicht.ende.hour,
                                       minute=feste_schicht.ende.minute) + timedelta(days=1)
                    if not check_au(datum=start,
                                    session=self.session) \
                            and not check_urlaub(datum=start,
                                                 session=self.session) \
                            and not check_au(datum=end - timedelta(minutes=1),
                                             session=self.session) \
                            and not check_urlaub(datum=end - timedelta(minutes=1),
                                                 session=self.session):
                        schicht_neu = Schicht(beginn=start,
                                              ende=end,
                                              asn=asn,
                                              assistent=self.assistent)
                        self.session.add(schicht_neu)
