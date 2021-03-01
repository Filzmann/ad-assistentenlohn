from sqlalchemy import select

from Model.adresse import Adresse
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.association_as_asn import AssociationAsAsn
from Model.einsatzbegleitung import EB
from Model.pflegefachkraft import PFK
from View.asn_edit_view import AsnEditView
from View.asn_stammdaten_view import AsnStammdatenView
from View.eb_view import EbView
from View.feste_schichten_view import FesteSchichtenView
from View.pfk_view import PfkView
from View.schicht_templates_view import SchichtTemplatesView


class AsnEditController:

    def __init__(self, parent_controller, session, assistent: Assistent = None, asn: ASN = None):
        self.parent = parent_controller
        self.parent_view = self.parent.view
        self.assistent = assistent
        self.asn = asn
        asnliste = [{'id': -1, 'kuerzel': 'Neuer ASN'}]
        for asn in assistent.asn:
            asnliste.append({"id": asn.asn.id, "kuerzel": asn.asn.kuerzel})
        self.view = AsnEditView(parent_view=self.parent_view, asn_liste=asnliste)

        for child in self.view.choose.winfo_children():
            child.config(command=self.change_asn)

        self.session = session
        self.view.stammdaten = AsnStammdatenView(parent_view=self.view.edit)

        self.ebliste = {0: "EB wählen oder neu anlegen"}
        for eb in self.session.query(EB).order_by(EB.name):
            self.ebliste[eb.id] = eb.vorname + " " + eb.name
        self.view.eb = EbView(parent_view=self.view.edit,
                              ebliste=self.ebliste)

        self.pfkliste = {0: "PFK wählen oder neu anlegen"}
        for pfk in self.session.query(PFK).order_by(PFK.name):
            self.pfkliste[pfk.id] = pfk.vorname + " " + pfk.name
        self.view.pfk = PfkView(parent_view=self.view.edit,
                                akt_pfk=self.asn.pfk if self.asn else None,
                                pfkliste=self.pfkliste)

        self.view.feste_schichten = FesteSchichtenView(parent_view=self.view.edit)
        self.view.templates = SchichtTemplatesView(parent_view=self.view.edit)

        self.view.draw()
        self.view.save_button.config(command=self.save_asn)
        # self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))

    def change_asn(self):
        # todo Reset für Neuer ASN nach update ASN
        if self.view.choose.selected_asn.get() > 0:
            new_asn_id = self.view.choose.selected_asn.get()
            for asn in self.session.query(ASN).filter(ASN.id == new_asn_id):
                self.asn = asn
        else:
            self.asn = None

        # Neubefüllen oder leeren der (Unter-)Formulare
        self.view.stammdaten.set_asn(asn=self.asn)
        self.view.feste_schichten.asn, self.view.templates.asn = self.asn, self.asn
        self.view.feste_schichten.set_feste_schichten()
        self.view.templates.set_schicht_templates()
        if self.asn:
            self.view.eb.set_eb(
                eb=self.asn.einsatzbegleitung if self.asn.einsatzbegleitung else None)
            self.view.pfk.set_pfk(
                pfk=self.asn.pflegefachkraft if self.asn.pflegefachkraft else None)
        else:
            # reset
            self.view.eb.set_eb()
            self.view.pfk.set_pfk()

    def change_eb(self, event=None):
        eb = self.view.eb.eb_dropdown.get()
        if not eb or eb == "0":
            self.view.eb.set_data(vorname='', name='', email='')
            self.asn.eb = None
        else:
            for eb in self.session.query(EB).filter(EB.id == eb):
                self.view.eb.set_data(vorname=eb.vorname, name=eb.name, email=eb.email)
                self.asn.eb = eb

    def set_asn(self, asn=None):
        if asn:
            home = None
            for result in self.session.query(ASN).filter(ASN.id == asn.id):
                self.asn = result

            for result in self.session.query(Adresse).filter(
                    Adresse.assistenznehmer == self.asn).filter(Adresse.bezeichner == '__home__'):
                home = result

            self.view.stammdaten.set_data(
                kuerzel=asn.kuerzel,
                vorname=asn.vorname,
                name=asn.name,
                email=asn.email,
                buero=asn.einsatzbuero,
                strasse=home.strasse,
                hnr=home.hausnummer,
                plz=home.plz,
                stadt=home.stadt)

            if self.asn.eb:
                self.view.eb.eb_dropdown.set(self.asn.eb.id)
                self.view.eb.set_data(
                    vorname=self.asn.eb.vorname,
                    name=self.asn.eb.name,
                    email=self.asn.eb.email,
                    eb_id=self.asn.eb.id
                )

            if self.asn.pfk:
                self.view.pfk.pfk_dropdown.set(self.asn.pfk.id)
                self.view.pfk.set_data(
                    vorname=self.asn.pfk.vorname,
                    name=self.asn.pfk.name,
                    email=self.asn.pfk.email,
                    pfk_id=self.asn.pfk.id
                )

        else:
            self.view.stammdaten.set_data(
                kuerzel="Neuer ASN",
                vorname='',
                name='',
                email='',
                buero=None,
                strasse='',
                hnr='',
                plz='',
                stadt='')

    def save_asn(self):
        self.asn = self.save_asn_stammdaten(assistent=self.assistent)

        self.asn.einsatzbegleitung = self.view.eb.save()
        self.asn.pflegefachkraft = self.view.pfk.save()
        self.session.commit()
        self.view.destroy()

    def save_asn_stammdaten(self, assistent):
        stammdaten = self.view.stammdaten.get_data()
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
