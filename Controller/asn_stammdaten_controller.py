from sqlalchemy.future import select
from Model.assistenznehmer import ASN
from View.asn_stammdaten_view import AsnStammdatenView


class AsnStammdatenController:
    def __init__(self, parent_controller, asn: ASN = None):
        self.parent = parent_controller
        self.view = AsnStammdatenView(parent_view=self.parent.view.edit)
        self.parent.view.edit.stammdaten = self.view

        self.session = self.parent.session
        if asn:
            result = self.session.execute(select(ASN).where(ASN.id == asn.id))
            asn = result.scalars().one()
            self.asn = asn
            self.view.set_data(
                kuerzel=asn.kuerzel,
                vorname=asn.vorname,
                name=asn.name,
                email=asn.email,
                strasse=asn.home.strasse,
                hnr=asn.home.hnr,
                plz=asn.home.plz,
                stadt=asn.home.stadt)

    def save(self):
        data = self.view.get_data()
        self.asn.vorname = data['vorname']
        self.asn.name = data['nachname']
        self.asn.email = data['email']
        self.asn.kuerzel = data['kuerzel']
        self.asn.home.strasse = data['strasse']
        self.asn.home.hnr = data['hnr']
        self.asn.home.plz = data['plz']
        self.asn.home.stadt = data['stadt']
