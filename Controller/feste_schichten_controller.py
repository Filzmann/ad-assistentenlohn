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
        feste_schichten = self.get_feste_schichten()

        self.view = FesteSchichtenView(parent_view=self.parent.view.edit,
                                       feste_schichten=feste_schichten)
        self.parent.view.edit.feste_schichten = self.view
        self.view.submit_button.config(command=self.save_feste_schicht)

        for kill_button in self.view.kill_buttons:
            kill_button['button'].config(command=lambda: self.delete_feste_schicht(feste_schicht_id=kill_button['id']))

    def get_feste_schichten(self):
        feste_schichten = []
        if not self.asn:
            return None
        for feste_schicht in self.asn.feste_schichten:
            if feste_schicht.asn == self.asn:
                feste_schichten.append({'id': feste_schicht.id,
                                        'wochentag': feste_schicht.wochentag,
                                        'beginn': feste_schicht.beginn,
                                        'ende': feste_schicht.ende,
                                        })
        return feste_schichten

    def save_feste_schicht(self):
        data = self.view.get_data()
        feste_schicht = FesteSchicht(#assistent=self.assistent,
                                     #asn=self.asn,
                                     wochentag=data['selected_day'],
                                     beginn=data['startzeit'],
                                     ende=data['endzeit']
                                     )
        self.session.add(feste_schicht)
        self.session.commit()
        self.assistent.feste_schichten.append(feste_schicht)
        self.asn.feste_schichten.append(feste_schicht)
        self.session.commit()
        self.view.draw(self.get_feste_schichten())



    def delete_feste_schicht(self, feste_schicht_id):
        pass
