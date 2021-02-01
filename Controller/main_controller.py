from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from Model.main_model import MainModel
from View.main_view import MainView
from Controller.begruessung_controller import BegruessungController
from Controller.hauptseite_controller import HauptseiteController
from sqlalchemy import create_engine, select
from Model.base import Base
from Model.schicht_templates import SchichtTemplates
from Model.weg import Weg
from Model.schicht import Schicht
from Model.assistent import Assistent
from View.menueleiste import Menuleiste


class MainController:
    def __init__(self):

        engine = create_engine("sqlite+pysqlite:///assistenten.db", echo=False, future=True, pool_pre_ping=True)
        self.Session = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(engine)

        self.model = MainModel()
        self.view = MainView()
        self.assistent = self.model.assistent

        with self.session_scope() as session:
            self.draw(session)
        self.view.mainloop()


    def oeffne_as(self, session, email=None):
        result = session.execute(select(Assistent).where(Assistent.email == email))
        self.model.assistent = result.scalars().one()

        self.draw(session)

    def draw(self, session):
        if self.view.inhalt:
            self.view.inhalt.destroy()

        if self.model.assistent:
            # wir haben einen Assistenten geladen
            menuleiste = Menuleiste(parent_view=self.view,
                                    assistent=self.model.assistent,
                                    parent_controller=self,
                                    session=session)
            self.view.config(menu=menuleiste)
            # die Hauptseite des Assistenten wird in die view eingehangen
            self.view.inhalt = HauptseiteController(
                session=session,
                assistent=self.model.assistent,
                parent_view=self.view
            ).view
            self.view.inhalt.grid()
        else:
            # ich speichere eine Referenz auf die View des Begrüßungs-Controllers in der Seiten-View, damit ich das
            # Layout von da aus steuern kann
            self.view.inhalt = BegruessungController(
                parent_controller=self,
                session=session,
                parent_view=self.view
            ).view
            self.view.inhalt.grid()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
