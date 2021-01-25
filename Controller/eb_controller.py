from sqlalchemy.future import select

from Model.einsatzbegleitung import EB
from View.eb_view import EbView


class EbController:
    def __init__(self, parent_controller, eb: EB = None):
        self.parent = parent_controller
        self.session = self.parent.session
        self.eb = eb
        self.ebliste = ["EB wählen oder neu anlegen"]
        result = self.session.execute(select(EB).order_by(EB.name))
        if result:
            ebs = result.scalars().all()
            for eb_item in ebs:
                self.ebliste.append(eb_item)
        self.view = EbView(parent_view=self.parent.view.edit, ebliste=self.ebliste, akt_eb=self.eb)

        self.parent.view.edit.eb = self.view

        if self.eb:
            result = self.session.execute(select(EB).where(EB.id == eb.id))
            eb = result.scalars().one()
            self.eb = eb
            self.view.selected.set(str(eb))
            self.view.set_data(vorname=eb.vorname,
                               name=eb.name,
                               email=eb.email)

    def save(self):

        data = self.view.get_data()

        if self.eb:
            #  Update
            self.eb.vorname = data['vorname']
            self.eb.name = data['name']
            self.eb.email = data['email']
        else:
            eb = EB(name=data['nachname'],
                    vorname=data['vorname'],
                    email=data['email'])
            self.session.add(eb)
            self.ebliste.append(eb)
            self.eb = eb

        return eb


