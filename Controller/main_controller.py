from sqlalchemy.orm import sessionmaker
from Model.main_model import MainModel
from View.main_view import MainView
from Controller.neuer_assistent_controller import NeuerAssistentController
from sqlalchemy import create_engine


class MainController:
    def __init__(self):

        engine = create_engine("sqlite+pysqlite:///assistenten.db", echo=True, future=True)
        self.Session = sessionmaker(bind=engine)
        self.callbacks = {}

        self.model = MainModel()
        self.view = MainView()
        self.assistent = None
        if self.model.assistent:
            self.view.draw_hauptseite()
        else:
            self.view.draw_begruessung()
            self.view.inhalt.button_neu.config(
                command=lambda: NeuerAssistentController(parent=self))

        self.view.mainloop()
