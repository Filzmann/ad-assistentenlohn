from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from View.schicht_view import SchichtView


class SchichtController:

    def __init__(self, parent_controller, session, assistent: Assistent = None, asn: ASN = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.asn = asn
        self.session = session

        asn_liste = self.get_asnliste()
        self.view = SchichtView(parent_view=self.parent.view,
                                asn_liste=asn_liste)



    def get_asnliste(self):
        # Todo implement
        return {'0': 'Neu'}
