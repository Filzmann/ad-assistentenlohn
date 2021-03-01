from sqlalchemy.future import select

from Model.adresse import Adresse
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.association_as_asn import AssociationAsAsn
from View.asn_stammdaten_view import AsnStammdatenView


class AsnStammdatenController:
    def __init__(self, parent_controller, parent_view, session, asn: ASN = None):
        self.parent_controller = parent_controller
        self.parent_view = parent_view
        self.view = AsnStammdatenView(parent_view=self.parent_view)
        self.asn = asn
        self.session = session



    def get_data(self):
        return self.view.get_data()
