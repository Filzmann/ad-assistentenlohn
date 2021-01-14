from sqlalchemy.future import select

from Model.einsatzbegleitung import EB
from View.eb_view import EbView


class EbController:
    def __init__(self, parent_controller, eb: EB = None):
        self.parent = parent_controller
        self.session = self.parent.session
        ebliste = ["EB wählen oder neu anlegen"]
        result = self.session.execute(select(EB).order_by(EB.name))
        if result:
            ebs = result.scalars().all()
            for eb_item in ebs:
                ebliste.append(eb_item)
        self.view = EbView(parent_view=self.parent.view.edit, ebliste=ebliste)
        self.parent.view.edit.eb = self.view

        if eb:
            result = self.session.execute(select(EB).where(EB.id == eb.id))
            eb = result.scalars().one()
            self.eb = eb
            self.view.selected.set(str(eb))
            self.view.set_data(vorname=eb.vorname,
                               name=eb.name,
                               email=eb.email)

    def save(self):
        data = self.view.get_data()
        self.eb.vorname = data['vorname']
        self.eb.name = data['nachname']
        self.eb.email = data['email']

    def get_eb(self):
        pass