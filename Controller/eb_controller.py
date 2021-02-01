from sqlalchemy.future import select
from Model.einsatzbegleitung import EB
from View.eb_view import EbView


class EbController:
    def __init__(self, parent_controller, session, eb: EB = None):
        self.parent = parent_controller
        self.session = session
        self.eb = eb
        self.ebliste = {"0": "EB wählen oder neu anlegen"}
        result = self.session.execute(select(EB).order_by(EB.name))
        if result:
            ebs = result.scalars().all()
            for eb_item in ebs:
                self.ebliste[str(eb_item.id)] = eb_item.vorname + " " + eb_item.name
        self.view = EbView(parent_view=self.parent.view.edit, ebliste=self.ebliste, akt_eb=self.eb)
        self.view.eb_dropdown.bind("<<ComboboxSelected>>", self.change_eb)

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
            eb = EB(name=data['name'],
                    vorname=data['vorname'],
                    email=data['email'])
            self.session.add(eb)
            self.ebliste[str(eb.id)] = eb.vorname + " " + eb.name
            self.eb = eb

        return self.eb
    
    def set_eb(self, eb=None):
        if eb:
            result = self.session.execute(select(EB).where(EB.id == eb.id))
            eb = result.scalars().one()
            self.eb = eb
            self.view.set_data(
                vorname=eb.vorname,
                name=eb.name,
                email=eb.email,
                eb_id=eb.id
            )
        else:
            self.eb = None
            self.view.set_data(
                vorname='',
                name='',
                email=''
            )


    def change_eb(self, event):
        eb = self.view.eb_dropdown.get()
        if not eb or eb == "0":
            self.view.set_data(vorname='', name='', email='')
            self.eb = None
        else:
            result = self.session.execute(select(EB).where(EB.id == eb))
            eb = result.scalars().one()
            self.set_eb(eb)

