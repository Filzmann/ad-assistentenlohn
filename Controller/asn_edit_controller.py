from Controller.asn_stammdaten_controller import AsnStammdatenController
from Controller.eb_controller import EbController
from Controller.feste_schichten_controller import FesteSchichtenController
from Controller.pfk_controller import PfkController
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from View.asn_edit_view import AsnEditView


class AsnEditController:

    def __init__(self, parent_controller, assistent: Assistent = None, asn: ASN = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.view = AsnEditView(parent_view=self.parent.view)
        self.asn = asn
        self.session = self.parent.Session()
        self.stammdaten = AsnStammdatenController(parent_controller=self,
                                                  asn=self.asn)
        self.view.eb = EbController(parent_controller=self)
        self.view.pfk = PfkController(parent_controller=self)
        self.view.feste_schichten = FesteSchichtenController(parent_controller=self)
        # self.view.templates = SchichtTemplatesController(parent_controller=self)
        self.view.edit.draw()

        # self.view.save_button.config(command=self.save_au)
        # self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))
        self.session = self.parent.Session()

