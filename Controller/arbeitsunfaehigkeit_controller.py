from datetime import datetime

from sqlalchemy import or_

from Model.arbeitsunfaehigkeit import AU
from Model.assistent import Assistent
from Model.schicht import Schicht
from View.arbeitsunfaehigkeit_view import AUView


class AUController:

    def __init__(self, parent_controller, session, assistent: Assistent = None, au: AU = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.view = AUView(parent_view=self.parent.view)
        self.au = au
        if self.au:
            self.view.set_data(beginn=self.au.beginn,
                               ende=self.au.ende
                               )
        self.view.save_button.config(command=self.save_au)
        self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))
        self.session = session

    def save_au(self, undneu=0):
        data = self.view.get_data()
        session = self.session
        ende = datetime(data['ende'].year, data['ende'].month, data['ende'].day, 23, 59)

        # falls in dem Zeitraum Schichten sind, müssen diese gelöscht werden
        for schicht in session.query(Schicht).filter(
                or_(
                    Schicht.beginn.between(data['beginn'], ende),
                    Schicht.ende.between(data['beginn'], ende)
                )):
            self.session.delete(schicht)

        if not self.au:

            au = AU(
                beginn=data['beginn'],
                ende=ende,
                assistent=self.assistent.id)

            session.add(au)

        else:
            self.au.beginn = data['beginn']
            self.au.ende = ende

        session.commit()
        self.view.destroy()
        self.parent.draw(session)

        if undneu == 1:
            AUController(self.parent, assistent=self.assistent, session=session)

