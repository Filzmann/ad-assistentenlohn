from Controller.infotext_controller import InfotextController
from Controller.navigation_controller import NavigationController
from Controller.summen_controller import SummenController
from Controller.tabelle_controller import TabelleController
from View.hauptseite_view import HauptseiteView


class HauptseiteController:
    def __init__(self, session, assistent, parent_view):
        as_name = assistent.vorname + " " + assistent.name
        self.view = HauptseiteView(parent_view=parent_view, as_name=as_name)
        self.assistent = assistent

        self.view.navigation = NavigationController(
            parent_controller=self,
            session=session,
            parent_view=self.view
        ).view
        self.view.navigation.grid()

        self.view.tabelle = TabelleController(
            parent_controller=self,
            session=session,
            parent_view=self.view
        ).view
        self.view.tabelle.grid()

        self.view.summen = SummenController(
            parent_controller=self,
            session=session,
            parent_view=self.view
        ).view
        self.view.summen.grid()

        self.view.infotext = InfotextController(
            parent_controller=self,
            session=session,
            parent_view=self.view
        ).view
        self.view.infotext.grid()
        self.view.draw()
