from sqlalchemy.future import select
from Model.pflegefachkraft import PFK
from View.pfk_view import PfkView


class PfkController:
    def __init__(self, parent_controller, pfk: PFK = None):
        self.parent = parent_controller
        self.session = self.parent.session
        pfkliste = ["PFK wählen oder neu anlegen"]
        result = self.session.execute(select(PFK).order_by(PFK.name))
        if result:
            pfks = result.scalars().all()
            for pfk_item in pfks:
                pfkliste.append(pfk_item)
        self.view = PfkView(parent_view=self.parent.view.edit, ebliste=pfkliste)
        self.parent.view.edit.pfk = self.view

        if pfk:
            result = self.session.execute(select(PFK).where(PFK.id == pfk.id))
            pfk = result.scalars().one()
            self.pfk = pfk
            self.view.selected.set(str(pfk))
            self.view.set_data(vorname=pfk.vorname,
                               name=pfk.name,
                               email=pfk.email)

    def save(self):
        data = self.view.get_data()
        self.pfk.vorname = data['vorname']
        self.pfk.name = data['nachname']
        self.pfk.email = data['email']

