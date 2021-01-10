from datetime import datetime

from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from View.asn_edit_view import ASNEditView


class ASNEditController:

    def __init__(self, parent_controller, assistent: Assistent = None, asn: ASN = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.view = ASNEditView(parent_view=self.parent.view)
        self.asn = asn


        # self.view.save_button.config(command=self.save_au)
        # self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))
        self.session = self.parent.Session()

    def save_au(self, undneu=0):
        data = self.view.get_data()
        session = self.session
        ende = datetime(data['ende'].year, data['ende'].month, data['ende'].day, 23, 59)



