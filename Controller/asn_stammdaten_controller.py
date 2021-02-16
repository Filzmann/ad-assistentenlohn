from sqlalchemy.future import select

from Model.adresse import Adresse
from Model.assistenznehmer import ASN
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

    def save(self):
        data = self.get_data()
        self.asn.vorname = data['vorname']
        self.asn.name = data['nachname']
        self.asn.email = data['email']
        self.asn.kuerzel = data['kuerzel']

        home_result = self.session.query(Adresse).filter(
            Adresse.assistenznehmer == self.asn).filter(
            Adresse.bezeichner == '__home__')
        if home_result:
            home = home_result.one()
            home.strasse = data['strasse']
            home.hausnummer = data['hausnummer']
            home.plz = data['plz']
            home.stadt = data['stadt']
        else:
            # new adress
            home = Adresse(
                strasse=data['strasse'],
                hausnummer=data['hausnummer'],
                plz=data['plz'],
                stadt=data['stadt'],
                bezeichner="__home__"
            )
            self.session.add(home)
            self.asn.adressbuch.append(home)
        self.session.commit()

    def get_data(self):
        return self.view.get_data()
