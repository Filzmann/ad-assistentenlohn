from sqlalchemy.future import select
from Model.assistenznehmer import ASN
from Model.schicht_templates import SchichtTemplate
from View.schicht_templates_view import SchichtTemplatesView


class SchichtTemplatesController:
    def __init__(self,
                 parent_controller,
                 parent_view,
                 session,
                 asn: ASN = None):
        self.asn = asn
        self.parent = parent_controller
        self.session = session
        schicht_templates = self.get_schicht_templates()

        self.view = SchichtTemplatesView(parent_view=parent_view,
                                         schicht_templates=schicht_templates)
        self.parent.view.edit.templates = self.view
        self.view.submit_button.config(command=self.save_schicht_template)

    def get_schicht_templates(self):
        schicht_templates = []
        if not self.asn:
            return None
        for schicht_template in self.asn.schicht_templates:
            if schicht_template.asn == self.asn:
                schicht_templates.append({'id': schicht_template.id,
                                          'bezeichner': schicht_template.bezeichner,
                                          'beginn': schicht_template.beginn,
                                          'ende': schicht_template.ende,
                                          })
        return schicht_templates

    def set_schicht_templates(self):
        if not self.asn:
            schicht_templates = []
        else:
            schicht_templates = self.get_schicht_templates()
        self.view.tabelle.destroy()
        self.view.draw(schicht_templates)
        for kill_button in self.view.kill_buttons:
            kill_button['button'].config(
                command=lambda: self.delete_schicht_template(schicht_template_id=kill_button['id']))

    def save_schicht_template(self):
        data = self.view.get_data()
        schicht_template = SchichtTemplate(asn=self.asn,
                                           bezeichner=data['bezeichner'],
                                           beginn=data['startzeit'],
                                           ende=data['endzeit']
                                           )
        self.session.add(schicht_template)
        self.session.commit()
        self.asn.schicht_templates.append(schicht_template)
        self.session.commit()
        self.set_schicht_templates()

    def delete_schicht_template(self, schicht_template_id):
        result = self.session.execute(select(SchichtTemplate).where(SchichtTemplate.id == schicht_template_id))
        schicht = result.scalars().one()
        self.session.delete(schicht)
        self.session.commit()
        self.set_schicht_templates()
