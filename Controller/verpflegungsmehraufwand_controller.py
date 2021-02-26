from datetime import datetime, timedelta

from sqlalchemy import or_, and_

from Helpers.help_functions import get_home, get_fahrzeit
from Model.assistent import Assistent
from Model.schicht import Schicht
from Model.urlaub import Urlaub
from Model.weg import Weg
from View.askhole_view import AskholeView
from View.urlaub_view import UrlaubView
from View.verpflegungsmehraufwand_view import VerpflegungsmehraufwandView


class VerpflegungsmehraufwandController:

    def __init__(self, parent_controller, session, assistent: Assistent):
        self.parent = parent_controller
        self.assistent = assistent
        self.session = session

        jahrarray = dict((jahr, jahr) for jahr in range(datetime.now().year, 1980, -1))
        self.akt_jahr = datetime.now().year - 1
        self.calculate()
        self.view = VerpflegungsmehraufwandView(parent_view=self.parent.view, jahrarray=jahrarray)
        self.view.jahr_dropdown.set(self.akt_jahr)

    def calculate(self):
        start = datetime(self.akt_jahr, 1, 1)
        end = datetime(self.akt_jahr + 1, 1, 1) - timedelta(seconds=1)
        for schicht in self.session.query(
                Schicht).filter(
            or_(
                Schicht.beginn.between(start, end),
                Schicht.ende.between(start, end)
            )
        ):
            dauer = (schicht.ende - schicht.beginn)

            as_home = get_home(assistent=self.assistent, session=self.session)
            if schicht.beginn_andere_adresse:
                beginn_adresse_einsatz = schicht.beginn_andere_adresse
            else:
                beginn_adresse_einsatz = get_home(asn=schicht.asn, session=self.session)
            zeit_hinfahrt = get_fahrzeit(adresse1=as_home, adresse2=beginn_adresse_einsatz, session=self.session)

            if not zeit_hinfahrt:
                self.view = AskholeView(self.parent.view, adresse1=as_home, adresse2=beginn_adresse_einsatz)
                break

            ende_adresse_einsatz = schicht.ende_andere_adresse if schicht.ende_andere_adresse \
                else get_home(schicht.asn)

            zeit_rueckfahrt = get_fahrzeit(adresse1=ende_adresse_einsatz, adresse2=as_home, session=self.session)

            if not zeit_hinfahrt:
                self.view = AskholeView(self.parent.view, adresse1=as_home, adresse2=ende_adresse_einsatz)
                break
            # TODO Randschichten prüfen, ob sie in anderes Jahr gehören (größter Anteil Stunden)
            # TODO kombinierte Schichten
        pass
