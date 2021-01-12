from sqlalchemy.future import select

from Model.schicht_wiederholend import SchichtRegelmaessig


class FesteSchichtenController:
    def __init__(self, parent_controller):
        self.parent = parent_controller
        self.session = self.parent.session
        ebliste = ["EB wählen oder neu anlegen"]
        result = self.session.execute(select(SchichtRegelmaessig).order_by(SchichtRegelmaessig.wochentag))
        if result:
            ebs = result.scalars().all()
            for eb_item in ebs:
                ebliste.append(eb_item)
        self.view = FesteSchichtenView(parent_view=self.parent.view.edit, ebliste=ebliste)
        self.parent.view.edit.eb = self.view