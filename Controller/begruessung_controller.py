from sqlalchemy.orm import sessionmaker
from Model.main_model import MainModel
from View.begruessungs_view import BegruessungsView
from Controller.assistent_controller import AssistentController
from sqlalchemy import create_engine, select
from Model.base import Base
from Model.assistent import Assistent


class BegruessungController:
    def __init__(self, session, parent_view, parent_controller):
        self.model = MainModel()
        self.parent_controller = parent_controller
        result = session.execute(select(Assistent).order_by(Assistent.name))
        session.commit()
        assistenten = result.scalars().all()
        assistentenliste = []
        for assistent in assistenten:
            assistentenliste.append(assistent.email)
        self.view = BegruessungsView(parent=parent_view, assistentenliste=assistentenliste)
        if assistentenliste:
            self.view.button_oeffnen.config(
                command=lambda: self.parent_controller.oeffne_as(email=self.view.get_selected())
            )
        self.view.button_neu.config(
            command=lambda: AssistentController(parent_controller=self.parent_controller))
