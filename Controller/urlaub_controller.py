from datetime import datetime

from sqlalchemy import or_

from Model.assistent import Assistent
from Model.schicht import Schicht
from Model.urlaub import Urlaub
from View.urlaub_view import UrlaubView


class UrlaubController:

    def __init__(self, parent_controller, session, assistent: Assistent = None, urlaub: Urlaub = None, nav_panel=None):
        self.parent = parent_controller
        self.assistent = assistent
        self.nav_panel = nav_panel
        self.view = UrlaubView(parent_view=self.parent.view)
        self.urlaub = urlaub
        if self.urlaub:
            self.view.set_data(beginn=self.urlaub.beginn,
                               ende=self.urlaub.ende,
                               status=self.urlaub.status)
        self.view.save_button.config(command=self.save_urlaub)
        self.view.saveandnew_button.config(command=lambda: self.save_urlaub(undneu=1))
        self.session = session

    def save_urlaub(self, undneu=0):
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

        if not self.urlaub:
            urlaub = Urlaub(
                beginn=data['beginn'],
                ende=ende,
                status=data['status'],
                assistent=self.assistent.id)

            session.add(urlaub)

        else:
            self.urlaub.beginn = data['beginn']
            self.urlaub.ende = ende
            self.urlaub.status = data['status']

        session.commit()
        self.view.destroy()
        if self.nav_panel:
            self.nav_panel.monat_change(datum=datetime(year=data['beginn'].year,
                                                       month=data['beginn'].month,
                                                       day=1),
                                        session=self.session)
        if undneu == 1:
            UrlaubController(self.parent, assistent=self.assistent, session=session)
