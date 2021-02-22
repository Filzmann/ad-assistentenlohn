from datetime import datetime

from sqlalchemy.future import select

from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.adresse import Adresse
from Model.association_as_asn import AssociationAsAsn
from Model.schicht import Schicht
from View.schicht_view import SchichtView


class SchichtController:

    def __init__(self, parent_controller, session,
                 assistent: Assistent = None,
                 asn: ASN = None,
                 edit_schicht: Schicht = None,
                 datum: datetime = None,
                 nav_panel=None
                 ):
        self.parent = parent_controller
        self.schicht = edit_schicht
        self.assistent = assistent
        self.asn = asn
        self.session = session
        self.nav_panel = nav_panel

        asn_liste = self.get_asnliste()
        adressliste = self.get_adressliste()
        self.view = SchichtView(parent_view=self.parent.view,
                                asn_liste=asn_liste, adressliste=adressliste)

        # bindings für dropdown-listen
        self.view.asn_dropdown.bind("<<ComboboxSelected>>", self.change_asn)
        self.view.abweichende_adresse_beginn_dropdown.bind("<<ComboboxSelected>>",
                                                           self.change_abweichende_adresse_beginn)
        self.view.abweichende_adresse_ende_dropdown.bind("<<ComboboxSelected>>",
                                                         self.change_abweichende_adresse_ende)

        # save button commands
        self.view.exit_button.config(command=self.view.destroy)
        self.view.save_button.config(command=self.save_schicht)
        self.view.saveandnew_button.config(command=lambda: self.save_schicht(undneu=True))

        if self.asn:
            self.view.set_data(asn=self.asn.id)

        if datum:
            self.view.set_data(beginn=datum, ende=datum)
        if edit_schicht:
            # Todo falls edit_schicht als id kommt noch aus der db holen
            self.view.set_data(
                asn=edit_schicht.asn.id,
                beginn=edit_schicht.beginn,
                ende=edit_schicht.ende,
                ist_at=edit_schicht.ist_assistententreffen,
                ist_pcg=edit_schicht.ist_pcg,
                ist_afg=edit_schicht.ist_ausfallgeld,
                ist_rb=edit_schicht.ist_kurzfristig
            )
        self.view.draw()
        # show/hide initialisieren
        if self.asn:
            self.view.hide(self.view.asn_stammdaten_form)
        self.change_asn()
        self.change_abweichende_adresse_beginn()
        self.change_abweichende_adresse_ende()

    def save_schicht(self, undneu=False):
        data = self.view.get_data()
        result = self.session.execute(select(Assistent).where(Assistent.id == self.assistent.id))
        assistent = result.scalars().one()

        if int(data['asn_id']) < 0:
            # neuer ASN
            # create new home
            home = Adresse(strasse=data['asn_stammdaten']['strasse'],
                           hausnummer=data['asn_stammdaten']['hnr'],
                           stadt=data['asn_stammdaten']['stadt'],
                           plz=data['asn_stammdaten']['plz'])
            # create new asn
            asn = ASN(
                kuerzel=data['asn_stammdaten']["kuerzel"],
                name=data['asn_stammdaten']["nachname"],
                vorname=data['asn_stammdaten']["vorname"],
                email=data['asn_stammdaten']["email"],
            )
            self.session.add(asn)
            asn.home = home

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
            self.session.commit()
            # der asn sollte beim commiten in der DB eine (auto)-id erhalten haben
            # diese kommt in den Datensatz und wird in die Schicht übernommen
            data['asn_id'] = asn.id

        schicht_asn = self.asn if self.asn else self.get_asn_by_id(int(data['asn_id']))
        startdatum_array = data['startdatum'].split('/')
        beginn = datetime(year=int(startdatum_array[2]),
                          month=int(startdatum_array[0]),
                          day=int(startdatum_array[1]),
                          hour=int(data['startzeit_stunde']),
                          minute=int(data['startzeit_minute']))
        enddatum_array = data['enddatum'].split('/')
        ende = datetime(year=int(enddatum_array[2]),
                        month=int(enddatum_array[0]),
                        day=int(enddatum_array[1]),
                        hour=int(data['endzeit_stunde']),
                        minute=int(data['endzeit_minute']))

        if self.schicht:
            self.schicht.beginn = beginn
            self.schicht.ende = ende
            self.schicht.ist_kurzfristig = data['ist rb']
            self.schicht.ist_ausfallgeld = data['ist afg']
            self.schicht.ist_pcg = data['ist pcg']
            self.schicht.ist_assistententreffen = data['ist at']

        else:
            schicht = Schicht(beginn=beginn,
                              ende=ende,
                              ist_kurzfristig=data['ist rb'],
                              ist_ausfallgeld=data['ist afg'],
                              ist_assistententreffen=data['ist at'],
                              ist_pcg=data['ist pcg']
                              )
            self.session.add(schicht)
            self.schicht = schicht
        self.session.commit()
        self.schicht.asn = schicht_asn
        self.schicht.assistent = assistent

        # TODO abweichende adressen
        # if int(data['abweichende_adresse_beginn']) > 0:
        # es wurde eine abweichende Adresse aus der Liste gewählt
        self.session.commit()

        # fenster zu
        self.view.destroy()

        if self.nav_panel:
            self.nav_panel.monat_change(datum=datetime(year=self.schicht.beginn.year,
                                                       month=self.schicht.beginn.month,
                                                       day=1),
                                        session=self.session)

        if undneu:
            parent = self.parent
            session = self.session
            assistent = self.assistent
            asn = self.asn
            datum = schicht.beginn

            self.schicht = None
            SchichtController(parent_controller=parent,
                              session=session,
                              assistent=assistent,
                              asn=asn,
                              edit_schicht=None,
                              datum=datum,
                              nav_panel=self.nav_panel)

    def get_asn_by_id(self, asn_id):
        result = self.session.execute(select(ASN).where(ASN.id == asn_id))
        if result:
            return result.scalars().one()
        return None

    def get_asnliste(self):
        asnliste = {-1: 'Neuer ASN'}
        # many to many....in der schleife wird die Assoziationstabelle durchgegangen
        # von asoc erhält man (zukünftig) extra-data wie "fester Mitarbeiter, Vertretung"
        # die sich nur auf die Beziehung zwischen AS und ASN beziehen. der asn selbst ist in
        # asoc.asn zu finden
        for asn_asoc in self.assistent.asn:
            asnliste[asn_asoc.asn.id] = asn_asoc.asn.kuerzel + ' - ' + asn_asoc.asn.vorname + ' ' + asn_asoc.asn.name
        return asnliste

    def get_adressliste(self):
        adressliste = {-2: 'Keine abweichende Adresse',
                       -1: 'Neu'}
        for adresse in self.session.query(Adresse).filter(
                Adresse.assistenznehmer == self.asn).filter(not Adresse.assistent):
            adressliste[adresse.id] = adresse.bezeichner + ": " \
                                      + adresse.strasse \
                                      + " " + adresse.hausnummer + ", " + adresse.plz + " " + adresse.stadt
        return adressliste

    def change_asn(self, event=None):
        if int(self.view.asn_dropdown.get()) < 0:
            self.view.show(self.view.asn_stammdaten_form)

        else:
            asn_id = int(self.view.asn_dropdown.get())
            asn = self.get_asn_by_id(asn_id)
            self.view.hide(self.view.asn_stammdaten_form)
            self.view.draw_templates(asn.schicht_templates)
            # Todo Set adressliste

    def change_abweichende_adresse_beginn(self, event=None):
        if int(self.view.abweichende_adresse_beginn_dropdown.get()) < -1:
            self.view.hide(self.view.abweichende_adresse_beginn)
        else:
            self.view.show(self.view.abweichende_adresse_beginn)

    def change_abweichende_adresse_ende(self, event=None):
        if int(self.view.abweichende_adresse_ende_dropdown.get()) < -1:
            self.view.hide(self.view.abweichende_adresse_ende)
        else:
            self.view.show(self.view.abweichende_adresse_ende)
