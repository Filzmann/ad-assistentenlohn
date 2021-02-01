from sqlalchemy import select
from Model.assistent import Assistent
from Model.adresse import Adresse
from View.assistent_new_edit_view import AssistentNewEditView


class AssistentController:

    def __init__(self, parent_controller, assistent: Assistent = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.view = AssistentNewEditView(parent=self.parent.view)
        self.view.save_button.config(command=self.save_assistent)
        self.session = self.parent.Session()
        if assistent:
            result = self.session.execute(select(Assistent).where(Assistent.id == assistent.id))
            assistent = result.scalars().one()
            self.assistent = assistent
            self.view.set_data(vorname=assistent.vorname,
                               name=assistent.name,
                               email=assistent.email,
                               einstellungsdatum=assistent.einstellungsdatum,
                               strasse=assistent.home.strasse,
                               hausnummer=assistent.home.hausnummer,
                               plz=assistent.home.plz,
                               stadt=assistent.home.stadt)

    def save_assistent(self):
        data = self.view.get_data()
        session = self.session

        if not self.assistent:
            home = Adresse(strasse=data['strasse'],
                           hausnummer=data['hausnummer'],
                           stadt=data['stadt'],
                           plz=data['plz'])

            assistent = Assistent(
                name=data['name'],
                vorname=data['vorname'],
                email=data['email'],
                einstellungsdatum=data['einstellungsdatum'],
            )

            assistent.home = home
            session.add(assistent)
            session.commit()
            self.view.destroy()
            self.parent.draw()
        else:
            self.assistent.name = data['name']
            self.assistent.vorname = data['vorname']
            self.assistent.email = data['email']
            self.assistent.home.strasse = data['strasse']
            self.assistent.home.hausnummer = data['hausnummer']
            self.assistent.home.plz = data['plz']
            self.assistent.home.stadt = data['stadt']

            self.view.destroy()
            self.parent.model.assistent = self.assistent
            self.parent.draw(self.session)

