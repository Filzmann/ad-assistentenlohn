from datetime import datetime
from sqlalchemy.orm import Session
from Model.assistent import Assistent
from Model.adresse import Adresse
from sqlalchemy import create_engine
from View.assistent_new_edit_view import AssistentNewEditView


class NeuerAssistentController:

    def __init__(self, parent):
        self.parent = parent
        self.session = parent.Session()
        self.view = AssistentNewEditView(parent=parent.view)
        self.view.save_button.config(command=self.save_assistent)

    def save_assistent(self, assistent=None):
        data = self.view.get_data()

        if not self.parent.assistent:
            home = Adresse(strasse=data['strasse'],
                           hausnummer=data['hausnummer'],
                           stadt=data['stadt'],
                           plz=data['plz'])
            self.session.add(home)
            assistent = Assistent(
                name=data['name'],
                vorname=data['vorname'],
                email=data['email'],
                einstellungsdatum=data['einstellungsdatum'],
                home=[home]

            )
            self.session.add(assistent)
            self.session.commit()
            pass
        # if not self.edit:
        #     assistent = AS(self.nachname_input.get(), self.vorname_input.get(),
        #                    self.email_input.get(), einstellungsdatum_date_obj)
        # else:
        #     assistent = self.assistent
        #     assistent.name = self.nachname_input.get()
        #     assistent.vorname = self.vorname_input.get()
        #     assistent.email = self.email_input.get()
        #
        # einstellungsdatum = self.einstellungsdatum_input.get_date()
        # assistent.einstellungsdatum = datetime.datetime.strptime(einstellungsdatum, "%m/%d/%y")
        # assistent.home = Adresse(kuerzel='home',
        #                           strasse=self.strasse_input.get(),
        #                           hnr=self.hausnummer_input.get(),
        #                           plz=self.plz_input.get(),
        #                           stadt=self.stadt_input.get())
        # assistent.__class__.assistent_is_loaded = 1
        #
        #
        # neu = 0 if self.edit == 1 else 1
        # assistent.save_to_file(neu=neu)
        # self.parent.fenster.redraw(assistent)
        # self.destroy()
        pass
