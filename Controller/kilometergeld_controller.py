from datetime import datetime, timedelta

from sqlalchemy import or_, and_

from Helpers.help_functions import get_home, get_fahrzeit, get_adresse_by_id, get_duration, get_entfernung
from Model.assistent import Assistent
from Model.schicht import Schicht
from Model.urlaub import Urlaub
from Model.weg import Weg
from View.askhole_view import AskholeView
from View.urlaub_view import UrlaubView
from View.kilometergeld_view import KilometergeldView


class KilometergeldController:

    def __init__(self, parent_controller, session, assistent: Assistent):
        self.parent = parent_controller
        self.assistent = assistent
        self.session = session
        self.view = None
        self.alle_unklarheiten_beseitigt = False
        self.data = {}

        jahrarray = dict((jahr, jahr) for jahr in range(datetime.now().year, 1980, -1))
        self.akt_jahr = datetime.now().year - 1
        self.calculate()
        if self.alle_unklarheiten_beseitigt:
            self.view = KilometergeldView(parent_view=self.parent.view, jahrarray=jahrarray, data=self.data)
            self.view.jahr_dropdown.set(self.akt_jahr)

    def calculate(self):
        start = datetime(self.akt_jahr, 1, 1)
        end = datetime(self.akt_jahr + 1, 1, 1) - timedelta(seconds=1)
        data = {}

        for schicht in self.session.query(
                Schicht).filter(
            or_(
                Schicht.beginn.between(start, end),
                Schicht.ende.between(start, end)
            )
        ):

            as_home = get_home(session=self.session, assistent=self.assistent)

            if schicht.beginn_andere_adresse:
                beginn_adresse_einsatz = get_adresse_by_id(session=self.session, adr_id=schicht.beginn_andere_adresse)
            else:
                beginn_adresse_einsatz = get_home(asn=schicht.asn, session=self.session)

            weg_hinfahrt = get_entfernung(adresse1=as_home, adresse2=beginn_adresse_einsatz, session=self.session)

            if not weg_hinfahrt:
                self.alle_unklarheiten_beseitigt = False
                self.view = AskholeView(self.parent.view, adresse1=as_home, adresse2=beginn_adresse_einsatz)
                self.view.button.config(command=lambda: self.save_askhole())
                break
            else:
                self.alle_unklarheiten_beseitigt = True
                self.insert_weg_in_data(adresse_1=as_home, adresse_2=beginn_adresse_einsatz)

            if schicht.ende_andere_adresse:
                ende_adresse_einsatz = get_adresse_by_id(session=self.session, adr_id=schicht.ende_andere_adresse)
            else:
                ende_adresse_einsatz = get_home(asn=schicht.asn, session=self.session)

            weg_rueckfahrt = get_fahrzeit(adresse1=ende_adresse_einsatz, adresse2=as_home, session=self.session)

            if not weg_rueckfahrt:
                self.alle_unklarheiten_beseitigt = False
                self.view = AskholeView(self.parent.view, adresse1=as_home, adresse2=ende_adresse_einsatz)
                self.view.button.config(command=lambda: self.save_askhole())
                break
            else:
                self.alle_unklarheiten_beseitigt = True
                self.insert_weg_in_data(adresse_1=as_home, adresse_2=ende_adresse_einsatz)
            # TODO Randschichten prüfen, ob sie in anderes Jahr gehören (größter Anteil Stunden)
            # TODO kombinierte Schichten

    def insert_weg_in_data(self, adresse_1, adresse_2):
        if str(adresse_1.id) + '-' + str(adresse_2.id) in self.data:
            key = str(adresse_1.id) + '-' + str(adresse_2.id)
            self.data[key]['count'] += 1
            self.data[key]['kmgeld'] += 0.3 * self.data[key]['entfernung']
        elif str(adresse_2.id) + '-' + str(adresse_1.id) in self.data:
            key = str(adresse_2.id) + '-' + str(adresse_1.id)
            self.data[key]['count'] += 1
            self.data[key]['kmgeld'] += 0.3 * self.data[key]['entfernung']
        else:
            key = str(adresse_1.id) + '-' + str(adresse_2.id)
            entfernung = get_entfernung(adresse1=adresse_1, adresse2=adresse_2, session=self.session)
            self.data[key] = {'adresse_1': adresse_1,
                              'adresse_2': adresse_2,
                              'count': 1,
                              'entfernung': entfernung,
                              'kmgeld': entfernung * 0.3
                              }

    def save_askhole(self):
        data = self.view.get_data()
        data['km'] = data['km'].replace(',', '.')
        neuer_weg = Weg(
            entfernung=float(data['km']),
            dauer_in_minuten=int(data['minuten']),
            adresse1_id=data['adresse1'].id,
            adresse2_id=data['adresse2'].id)
        self.session.add(neuer_weg)
        self.session.commit()
        self.view.destroy()
        self.calculate()
