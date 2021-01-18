from sqlalchemy.future import select

from Controller.asn_stammdaten_controller import AsnStammdatenController
from Controller.eb_controller import EbController
from Controller.feste_schichten_controller import FesteSchichtenController
from Controller.pfk_controller import PfkController
from Model.adresse import Adresse
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.association_as_asn import AssociationAsAsn
from View.asn_edit_view import AsnEditView


class AsnEditController:

    def __init__(self, parent_controller, assistent: Assistent = None, asn: ASN = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.asn = asn
        asnliste = []
        for asn in assistent.asn:
            asnliste.append({"id": asn.asn.id, "kuerzel": asn.asn.kuerzel})
        self.view = AsnEditView(parent_view=self.parent.view, asn_liste=asnliste)
        for child in self.view.choose.winfo_children():
            child.config(command=self.change_asn)

        self.session = self.parent.Session()
        self.stammdaten = AsnStammdatenController(parent_controller=self, asn=self.asn)
        self.view.eb = EbController(parent_controller=self)
        self.view.pfk = PfkController(parent_controller=self)
        self.view.feste_schichten = FesteSchichtenController(parent_controller=self)
        # self.view.templates = SchichtTemplatesController(parent_controller=self)
        self.view.edit.draw()
        self.view.edit.save_button.config(command=self.save_asn)
        # self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))
        self.session = self.parent.Session()

    def change_asn(self):
        self.asn = self.view.choose.selected_asn
        self.stammdaten = AsnStammdatenController(parent_controller=self, asn=self.asn)


    def save_asn(self):
        stammdaten = self.stammdaten.get_data()
        if not self.asn:
            home = Adresse(strasse=stammdaten['strasse'],
                           hausnummer=stammdaten['hnr'],
                           stadt=stammdaten['stadt'],
                           plz=stammdaten['plz'])
            asn = ASN(
                kuerzel=stammdaten["kuerzel"],
                name=stammdaten["nachname"],
                vorname=stammdaten["vorname"],
                email=stammdaten["email"],

            )
            asn.home = home
            self.session.add(asn)

            # many_2_many as - asn
            # 1. Zusatzdaten in Asociation,
            # 2. ASN der  Aso zuweisen,
            # 3. Aso dem Assistenten
            # Todo auswahl fest/vertretung/feste_vertretung
            result = self.session.execute(select(Assistent).where(Assistent.id == self.assistent.id))
            assistent = result.scalars().one()
            association = AssociationAsAsn(fest_vertretung="fest")
            association.asn = asn
            association.as_id = assistent.id
            asn.assistenten.append(association)


        # eb=self.view.eb.get_eb()
        # pfk=self.view.pfk.get_pfk()
        self.session.commit()