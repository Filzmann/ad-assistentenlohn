from sqlalchemy.future import select
from Model.pflegefachkraft import PFK
from View.pfk_view import PfkView


class PfkController:
    def __init__(self, parent_controller, session, pfk: PFK = None):
        self.parent = parent_controller
        self.session = session
        self.pfk = pfk
        self.pfkliste = {0: "PFK wählen oder neu anlegen"}
        result = self.session.execute(select(PFK).order_by(PFK.name))
        if result:
            pfks = result.scalars().all()
            for pfk_item in pfks:
                self.pfkliste[pfk_item.id] = pfk_item.vorname + " " + pfk_item.name
        self.view = PfkView(parent_view=self.parent.view.edit, pfkliste=self.pfkliste, akt_pfk=self.pfk)
        self.view.pfk_dropdown.bind("<<ComboboxSelected>>", self.change_pfk)

        self.parent.view.edit.pfk = self.view

        if self.pfk:
            result = self.session.execute(select(PFK).where(PFK.id == pfk.id))
            pfk = result.scalars().one()
            self.pfk = pfk
            self.view.selected.set(pfk)
            self.view.set_data(vorname=pfk.vorname,
                               name=pfk.name,
                               email=pfk.email)

    def save(self):

        data = self.view.get_data()

        if self.pfk:
            #  Update
            self.pfk.vorname = data['vorname']
            self.pfk.name = data['name']
            self.pfk.email = data['email']
        else:
            pfk = PFK(name=data['name'],
                      vorname=data['vorname'],
                      email=data['email'])
            self.session.add(pfk)
            self.pfkliste[pfk.id] = pfk.vorname + " " + pfk.name
            self.pfk = pfk
        self.session.commit()
        return self.pfk

    def set_pfk(self, pfk=None):
        if pfk:
            result = self.session.execute(select(PFK).where(PFK.id == pfk.id))
            pfk = result.scalars().one()
            self.pfk = pfk
            self.view.set_data(
                vorname=pfk.vorname,
                name=pfk.name,
                email=pfk.email,
                pfk_id=pfk.id
            )
        else:
            self.pfk = None
            self.view.set_data(
                vorname='',
                name='',
                email='',
                pfk_id="0"
            )


    def change_pfk(self, event=None):
        pfk = self.view.pfk_dropdown.get()
        if not pfk or pfk == "0":
            self.view.set_data(vorname='', name='', email='')
            self.pfk = None
        else:
            result = self.session.execute(select(PFK).where(PFK.id == pfk))
            pfk = result.scalars().one()
            self.set_pfk(pfk)

