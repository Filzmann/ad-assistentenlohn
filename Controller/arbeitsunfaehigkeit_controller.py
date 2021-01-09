from datetime import datetime

from Model.arbeitsunfaehigkeit import AU
from Model.assistent import Assistent
from View.arbeistsunfaehigkeit_view import AUView


class AUController:

    def __init__(self, parent_controller, assistent: Assistent = None, au: AU = None):
        self.parent = parent_controller
        self.assistent = assistent
        self.view = AUView(parent=self.parent.view)
        self.au = au
        self.view.save_button.config(command=self.save_au)
        self.view.saveandnew_button.config(command=lambda: self.save_au(undneu=1))
        self.session = self.parent.Session()

    def save_au(self, undneu=0):
        data = self.view.get_data()
        session = self.session
        ende = datetime(data['ende'].year, data['ende'].month, data['ende'].day, 23, 59)

        if not self.au:

            au = AU(
                beginn=data['beginn'],
                ende=ende,
                assistent=self.assistent.id)

            session.add(au)
            session.commit()
            self.view.destroy()
            self.parent.draw()
        else:
            self.au.beginn = data['beginn'],
            self.au.ende = ende

            session.commit()
            self.view.destroy()
        if undneu == 1:
            AUController(self.parent, assistent=self.assistent)

