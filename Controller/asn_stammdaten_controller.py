from sqlalchemy.future import select

from Model.adresse import Adresse
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.association_as_asn import AssociationAsAsn
from View.asn_stammdaten_view import AsnStammdatenView


class AsnStammdatenController:
    def __init__(self, parent_controller, session, asn: ASN = None):
        self.parent = parent_controller
        self.view = AsnStammdatenView(parent_view=self.parent.view.edit)
        self.parent.view.edit.stammdaten = self.view
        self.asn = asn
        self.session = session

    def set_asn(self, asn=None):
        if asn:
            result = self.session.execute(select(ASN).where(ASN.id == asn.id))
            asn = result.scalars().one()

            self.asn = asn
            home = self.session.query(Adresse).filter(
                Adresse.assistenznehmer == self.asn).filter(
                Adresse.bezeichner == '__home__').one()
            self.view.set_data(
                kuerzel=asn.kuerzel,
                vorname=asn.vorname,
                name=asn.name,
                email=asn.email,
                buero=asn.einsatzbuero,
                strasse=home.strasse,
                hnr=home.hausnummer,
                plz=home.plz,
                stadt=home.stadt)
        else:
            self.view.set_data(
                kuerzel="Neuer ASN",
                vorname='',
                name='',
                email='',
                buero=None,
                strasse='',
                hnr='',
                plz='',
                stadt='')

    def save_asn(self, assistent):
        stammdaten = self.get_data()
        if self.asn:
            self.asn.kuerzel = stammdaten['kuerzel']
            self.asn.vorname = stammdaten['vorname']
            self.asn.name = stammdaten['nachname']
            self.asn.email = stammdaten['email']
            self.asn.einsatzbuero = stammdaten['buero']

            home = self.session.query(Adresse).filter(
                Adresse.assistenznehmer == self.asn).filter(
                Adresse.bezeichner == '__home__').one()

            home.strasse = stammdaten['strasse']
            home.hausnummer = stammdaten['hnr']
            home.plz = stammdaten['plz']
            home.stadt = stammdaten['stadt']

        else:
            # create new home
            home = Adresse(strasse=stammdaten['strasse'],
                           hausnummer=stammdaten['hnr'],
                           stadt=stammdaten['stadt'],
                           plz=stammdaten['plz'],
                           bezeichner="__home__")

            # create new asn
            asn = ASN(
                kuerzel=stammdaten["kuerzel"],
                name=stammdaten["nachname"],
                vorname=stammdaten["vorname"],
                email=stammdaten["email"],

            )
            # connect
            asn.adressbuch.append(home)
            self.session.add(asn)

            # many_2_many as - asn
            # 1. Zusatzdaten in Asociation,
            # 2. ASN der  Aso zuweisen,
            # 3. Aso dem Assistenten
            # Todo auswahl fest/vertretung/feste_vertretung
            result = self.session.execute(select(Assistent).where(Assistent.id == assistent.id))
            assistent = result.scalars().one()
            association = AssociationAsAsn(fest_vertretung="fest")
            association.asn = asn
            association.as_id = assistent.id
            asn.assistenten.append(association)
            self.asn = asn

        return self.asn

    def get_data(self):
        return self.view.get_data()
