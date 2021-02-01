from sqlalchemy.future import select

from Model.assistent import Assistent
from Model.assistenznehmer import ASN
from Model.feste_schichten import FesteSchicht
from View.feste_schichten_view import FesteSchichtenView


class FesteSchichtenController:
    def __init__(self,
                 parent_controller,
                 session,
                 assistent: Assistent = None,
                 asn: ASN = None):
        self.asn = asn
        self.assistent = assistent
        self.parent = parent_controller
        self.session = session
        result = self.session.execute(
            select(FesteSchicht).where(
                Assistent == self.assistent).where(
                ASN == self.asn).order_by(FesteSchicht.wochentag)

        )
        if result:
            feste_schichten = result.scalars().all()

        self.view = FesteSchichtenView(parent_view=self.parent.view.edit,
                                       feste_schichten=feste_schichten)
        self.parent.view.edit.feste_schichten = self.view
        self.view.submit_button.config(command=self.save_feste_schicht)

        for kill_button in self.view.kill_buttons:
            kill_button['button'].config(command=lambda: self.delete_feste_schicht(feste_schicht_id=kill_button['id']))

    def save_feste_schicht(self):
        data = self.view.get_data()
        feste_schicht = FesteSchicht(assistent=self.assistent.id,
                                     asn=self.asn.id,
                                     wochentag=data['selected_day'],
                                     beginn=data['startzeit'],
                                     ende=data['endzeit']
                                     )
        self.session.add(feste_schicht)

    def delete_feste_schicht(self, feste_schicht_id):
        pass
