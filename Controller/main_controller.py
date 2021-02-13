from datetime import datetime

from sqlalchemy.orm import sessionmaker
from Model.main_model import MainModel
from View.main_view import MainView
from Controller.begruessung_controller import BegruessungController
from Controller.hauptseite_controller import HauptseiteController
from sqlalchemy import create_engine, select, event
from Model.base import Base
from Model.schicht_templates import SchichtTemplate
from Model.weg import Weg
from Model.schicht import Schicht
from Model.assistent import Assistent
from Model.lohn import Lohn
from View.menueleiste import Menuleiste

engine = create_engine('sqlite:///assistenten.db', echo=True)
Session = sessionmaker(engine)


@event.listens_for(Lohn.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    with Session() as session:

        # TV Tabelle 2021
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=1,
            grundlohn=15.22,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=2,
            grundlohn=16.47,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=3,
            grundlohn=17.19,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=4,
            grundlohn=17.86,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=5,
            grundlohn=18.40,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2021, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=6,
            grundlohn=18.77,
            nacht_zuschlag=3.44,
            samstag_zuschlag=3.44,
            sonntag_zuschlag=4.30,
            feiertag_zuschlag=6.01,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=5.16,
            hl_abend_zuschlag=6.01,
            silvester_zuschlag=6.01
        ))

        # TV Tabelle 2020
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=1,
            grundlohn=14.92,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=2,
            grundlohn=16.18,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=3,
            grundlohn=16.89,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=4,
            grundlohn=17.56,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=5,
            grundlohn=18.11,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))
        session.add(Lohn(
            gueltig_ab=datetime(2020, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=6,
            grundlohn=18.47,
            nacht_zuschlag=3.38,
            samstag_zuschlag=3.38,
            sonntag_zuschlag=4.22,
            feiertag_zuschlag=5.91,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.91,
            silvester_zuschlag=5.91
        ))

        # TV Tabelle 2019 Fallback
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=1,
            grundlohn=14.31,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=2,
            grundlohn=15.64,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=3,
            grundlohn=16.35,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=4,
            grundlohn=17.02,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=5,
            grundlohn=17.56,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.add(Lohn(
            gueltig_ab=datetime(1970, 1, 1),
            eingruppierung=5,
            erfahrungsstufe=6,
            grundlohn=17.91,
            nacht_zuschlag=3.27,
            samstag_zuschlag=3.27,
            sonntag_zuschlag=4.09,
            feiertag_zuschlag=5.72,
            wechselschicht_zuschlag=0.63,
            orga_zuschlag=0.20,
            ueberstunden_zuschlag=4.48,
            hl_abend_zuschlag=5.72,
            silvester_zuschlag=5.72
        ))
        session.commit()
        session.close()


Base.metadata.create_all(bind=engine)


class MainController:
    def __init__(self):

        self.model = MainModel()
        self.view = MainView()
        self.assistent = self.model.assistent
        self.inhalt = None
        with Session() as session:
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

            # die Hauptseite des Assistenten wird in die view eingehangen
            self.inhalt = HauptseiteController(
                session=session,
                assistent=self.model.assistent,
                parent_view=self.view,
                parent_controller=self
            )
            self.view.inhalt = self.inhalt.view
            self.view.inhalt.grid()
            menuleiste = Menuleiste(parent_view=self.view,
                                    assistent=self.model.assistent,
                                    parent_controller=self,
                                    session=session,
                                    nav_panel=self.inhalt.navigation)
            self.view.config(menu=menuleiste)
        else:
            # ich speichere eine Referenz auf die View des Begrüßungs-Controllers in der Seiten-View, damit ich das
            # Layout von da aus steuern kann
            self.inhalt = BegruessungController(
                parent_controller=self,
                session=session,
                parent_view=self.view
            )
            self.view.inhalt = self.inhalt.view
            self.view.inhalt.grid()
