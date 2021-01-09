from sqlalchemy.orm import sessionmaker
from Model.main_model import MainModel
from View.main_view import MainView
from Controller.begruessung_controller import BegruessungController
from Controller.hauptseite_controller import HauptseiteController
from sqlalchemy import create_engine, select
from Model.base import Base
from Model.assistent import Assistent
from View.menueleiste import Menuleiste


class MainController:
    def __init__(self):

        engine = create_engine("sqlite+pysqlite:///assistenten.db", echo=True, future=True)
        self.Session = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(engine)
        self.model = MainModel()
        self.view = MainView()
        self.assistent = self.model.assistent
        self.draw()
        self.view.mainloop()

    def oeffne_as(self, email=None):
        session = self.Session()
        result = session.execute(select(Assistent).where(Assistent.email == email))
        self.model.assistent = result.scalars().one()
        self.draw()

    def draw(self):
        if self.view.inhalt:
            self.view.inhalt.destroy()

        if self.model.assistent:
            menuleiste = Menuleiste(parent_view=self.view,
                                    assistent=self.model.assistent,
                                    parent_controller=self)
            self.view.config(menu=menuleiste)
            self.view.inhalt = HauptseiteController(
                session_maker=self.Session,
                assistent=self.model.assistent,
                parent_view=self.view
            ).view
            self.view.inhalt.grid()
        else:
            # ich speichere eine Referenz auf die View des Begrüßungs-Controllers in der Seiten-View, damit ich das
            # Layout von da aus steuern kann
            self.view.inhalt = BegruessungController(
                parent_controller=self,
                session_maker=self.Session,
                parent_view=self.view
            ).view
            self.view.inhalt.grid()
