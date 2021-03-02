from sqlalchemy import select

from Model.adresse import Adresse
from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.association_as_asn import AssociationAsAsn
from Model.einsatzbegleitung import EB
from Model.feste_schichten import FesteSchicht
from Model.pflegefachkraft import PFK
from Model.schicht_templates import SchichtTemplate
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
        self.session = session

        # Daten Für Auswahl ASN
        asnliste = [{'id': -1, 'kuerzel': 'Neuer ASN'}]
        for asn in assistent.asn:
            asnliste.append({"id": asn.asn.id, "kuerzel": asn.asn.kuerzel})
        self.view = AsnEditView(parent_view=self.parent_view, asn_liste=asnliste)

        # jeder ASN-Radiobutton bekommt das Command
        for child in self.view.choose.winfo_children():
            child.config(command=self.change_asn)

        self.view.stammdaten = AsnStammdatenView(parent_view=self.view.edit)

        self.ebliste = {0: "EB wählen oder neu anlegen"}
        for eb in self.session.query(EB).order_by(EB.name):
            self.ebliste[eb.id] = eb.vorname + " " + eb.name
        self.view.eb = EbView(parent_view=self.view.edit,
                              ebliste=self.ebliste)
        self.view.eb.eb_dropdown.bind("<<ComboboxSelected>>", self.change_eb)

        self.pfkliste = {0: "PFK wählen oder neu anlegen"}
        for pfk in self.session.query(PFK).order_by(PFK.name):
            self.pfkliste[pfk.id] = pfk.vorname + " " + pfk.name
        self.view.pfk = PfkView(parent_view=self.view.edit,
                                akt_pfk=self.asn.pfk if self.asn else None,
                                pfkliste=self.pfkliste)
        self.view.pfk.pfk_dropdown.bind("<<ComboboxSelected>>", self.change_pfk)

        self.view.feste_schichten = FesteSchichtenView(parent_view=self.view.edit)
        self.view.feste_schichten.submit_button.config(command=self.save_feste_schicht)
        self.view.templates = SchichtTemplatesView(parent_view=self.view.edit)
        self.view.templates.submit_button.config(command=self.save_schicht_template)

        self.view.draw()
        self.view.save_button.config(command=self.save_asn)
        # self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))

    def change_asn(self):
        # todo Reset für Neuer ASN nach update ASN
        if self.view.selected_asn.get() > 0:
            new_asn_id = self.view.selected_asn.get()
            for asn in self.session.query(ASN).filter(ASN.id == new_asn_id):
                self.asn = asn
        else:
            self.asn = None

        # Neubefüllen oder leeren der (Unter-)Formulare
        self.set_asn(asn=self.asn)

        self.set_feste_schichten()
        self.set_schicht_templates()

        if self.asn and hasattr(self.asn, 'einsatzbegleitung'):
            if self.asn.einsatzbegleitung:
                self.view.eb.set_data(
                    vorname=self.asn.einsatzbegleitung.vorname,
                    name=self.asn.einsatzbegleitung.name,
                    email=self.asn.einsatzbegleitung.email,
                    eb_id=self.asn.einsatzbegleitung.id
                )
            else:
                # reset TODO 2 x Reset, schöner lösen
                self.view.eb.set_data(
                    vorname='',
                    name='',
                    email=''
                )
        else:
            # reset
            self.view.eb.set_data(
                vorname='',
                name='',
                email=''
            )

        if self.asn and hasattr(self.asn, 'pflegefachkraft'):
            if self.asn.pflegefachkraft:
                self.view.pfk.set_data(
                    vorname=self.asn.pflegefachkraft.vorname,
                    name=self.asn.pflegefachkraft.name,
                    email=self.asn.pflegefachkraft.email,
                    pfk_id=self.asn.pflegefachkraft.id
                )
            else:
                # reset TODO 2 x Reset, schöner lösen

                self.view.pfk.set_data(
                    vorname='',
                    name='',
                    email=''
                )
        else:
            # reset
            self.view.pfk.set_data(
                vorname='',
                name='',
                email=''
            )

    def change_eb(self, event=None):
        eb = self.view.eb.eb_dropdown.get()
        if not eb or eb == "0":
            self.view.eb.set_data(vorname='', name='', email='')
            self.asn.eb = None
        else:
            # Todo Wenn noch kein ASN kann EB da auch nicht gespeichert werden. Zwischenspeichern?
            for eb in self.session.query(EB).filter(EB.id == eb):
                self.view.eb.set_data(vorname=eb.vorname, name=eb.name, email=eb.email)
                self.asn.eb = eb
                
    def change_pfk(self, event=None):
        pfk = self.view.pfk.pfk_dropdown.get()
        if not pfk or pfk == "0":
            self.view.pfk.set_data(vorname='', name='', email='')
            self.asn.pfk = None
        else:
            # Todo Wenn noch kein ASN kann pfk da auch nicht gespeichert werden. Zwischenspeichern?
            for pfk in self.session.query(PFK).filter(PFK.id == pfk):
                self.view.pfk.set_data(vorname=pfk.vorname, name=pfk.name, email=pfk.email)
                self.asn.pfk = pfk

    def get_feste_schichten(self):
        feste_schichten = []
        if not self.asn:
            return None
        for feste_schicht in self.asn.feste_schichten:
            if feste_schicht.asn == self.asn:
                feste_schichten.append({'id': feste_schicht.id,
                                        'wochentag': feste_schicht.wochentag,
                                        'beginn': feste_schicht.beginn,
                                        'ende': feste_schicht.ende,
                                        })
        return feste_schichten

    def get_schicht_templates(self):
        schicht_templates = []
        if not self.asn:
            return None
        for schicht_template in self.asn.schicht_templates:
            if schicht_template.asn == self.asn:
                schicht_templates.append({'id': schicht_template.id,
                                          'bezeichner': schicht_template.bezeichner,
                                          'beginn': schicht_template.beginn,
                                          'ende': schicht_template.ende,
                                          })
        return schicht_templates

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

            if self.asn.einsatzbegleitung:
                self.view.eb.eb_dropdown.set(self.asn.einsatzbegleitung.id)
                self.view.eb.set_data(
                    vorname=self.asn.einsatzbegleitung.vorname,
                    name=self.asn.einsatzbegleitung.name,
                    email=self.asn.einsatzbegleitung.email,
                    eb_id=self.asn.einsatzbegleitung.id
                )

            if self.asn.pflegefachkraft:
                self.view.pfk.pfk_dropdown.set(self.asn.pflegefachkraft.id)
                self.view.pfk.set_data(
                    vorname=self.asn.pflegefachkraft.vorname,
                    name=self.asn.pflegefachkraft.name,
                    email=self.asn.pflegefachkraft.email,
                    pfk_id=self.asn.pflegefachkraft.id
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

    def set_feste_schichten(self):
        if not self.asn:
            feste_schichten = []
        else:
            feste_schichten = self.get_feste_schichten()
        self.view.feste_schichten.tabelle.destroy()
        self.view.feste_schichten.draw(feste_schichten)
        for kill_button in self.view.feste_schichten.kill_buttons:
            kill_button['button'].config(command=lambda: self.delete_feste_schicht(feste_schicht_id=kill_button['id']))

    def set_schicht_templates(self):
        if not self.asn:
            schicht_templates = []
        else:
            schicht_templates = self.get_schicht_templates()
        self.view.templates.tabelle.destroy()
        self.view.templates.draw(schicht_templates)
        for kill_button in self.view.templates.kill_buttons:
            kill_button['button'].config(
                command=lambda: self.delete_schicht_template(schicht_template_id=kill_button['id']))

    def save_asn(self):
        self.asn = self.save_asn_stammdaten(assistent=self.assistent)
        # Einsatzbegleitung Speichern
        eb_data = self.view.eb.get_data()
        if eb_data['id'] > 0:
            # update
            for eb in self.session.query(EB).filter(EB.id == eb_data['id']):
                self.asn.einsatzbegleitung = eb
                self.asn.einsatzbegleitung.name = eb_data['name']
                self.asn.einsatzbegleitung.vorname = eb_data['vorname']
                self.asn.einsatzbegleitung.email = eb_data['email']

        else:
            # new
            if eb_data['name'] or eb_data['vorname'] or eb_data['email']:
                eb = EB(name=eb_data['name'],
                        vorname=eb_data['vorname'],
                        email=eb_data['email'])
                self.session.add(eb)
                self.session.commit()
                self.session.refresh(eb)
                self.asn.einsatzbegleitung = eb

        # Einsatzbegleitung Speichern
        pfk_data = self.view.pfk.get_data()
        if pfk_data['id'] > 0:
            # update
            for pfk in self.session.query(PFK).filter(PFK.id == pfk_data['id']):
                self.asn.pflegefachkraft = pfk
                self.asn.pflegefachkraft.name = pfk_data['name']
                self.asn.pflegefachkraft.vorname = pfk_data['vorname']
                self.asn.pflegefachkraft.email = pfk_data['email']
        else:
            # new
            if pfk_data['name'] or pfk_data['vorname'] or pfk_data['email']:
                pfk = PFK(name=pfk_data['name'],
                          vorname=pfk_data['vorname'],
                          email=pfk_data['email'])
                self.session.add(pfk)
                self.session.commit()
                self.session.refresh(pfk)
                self.asn.pflegefachkraft = pfk
        self.session.commit()
        self.view.destroy()

    def save_asn_stammdaten(self, assistent):
        stammdaten = self.view.stammdaten.get_data()
        if self.asn:
            self.asn.kuerzel = stammdaten['kuerzel']
            self.asn.vorname = stammdaten['vorname']
            self.asn.name = stammdaten['name']
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
                name=stammdaten["name"],
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

    def save_feste_schicht(self):
        data = self.view.feste_schichten.get_data()
        feste_schicht = FesteSchicht(assistent=self.assistent,
                                     asn=self.asn,
                                     wochentag=data['selected_day'],
                                     beginn=data['startzeit'],
                                     ende=data['endzeit']
                                     )
        self.session.add(feste_schicht)
        self.session.commit()
        self.assistent.feste_schichten.append(feste_schicht)
        self.asn.feste_schichten.append(feste_schicht)
        self.session.commit()
        self.set_feste_schichten()

    def save_schicht_template(self):
        data = self.view.templates.get_data()
        schicht_template = SchichtTemplate(asn=self.asn,
                                           bezeichner=data['bezeichner'],
                                           beginn=data['startzeit'],
                                           ende=data['endzeit']
                                           )
        self.session.add(schicht_template)
        self.session.commit()
        self.asn.schicht_templates.append(schicht_template)
        self.session.commit()
        self.set_schicht_templates()

    def delete_schicht_template(self, schicht_template_id):
        result = self.session.execute(select(SchichtTemplate).where(SchichtTemplate.id == schicht_template_id))
        schicht = result.scalars().one()
        self.session.delete(schicht)
        self.session.commit()
        self.set_schicht_templates()

    def delete_feste_schicht(self, feste_schicht_id):
        result = self.session.execute(select(FesteSchicht).where(FesteSchicht.id == feste_schicht_id))
        schicht = result.scalars().one()
        self.session.delete(schicht)
        self.session.commit()
        self.set_feste_schichten()
