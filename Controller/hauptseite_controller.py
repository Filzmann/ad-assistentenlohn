from Controller.infotext_controller import InfotextController
from Controller.navigation_controller import NavigationController
from Controller.summen_controller import SummenController
from Controller.tabelle_controller import TabelleController
from View.hauptseite_view import HauptseiteView


class HauptseiteController:
    def __init__(self, session, assistent, parent_view, root_window_controller, parent_controller=None, ):
        as_name = assistent.vorname + " " + assistent.name
        self.view = HauptseiteView(parent_view=parent_view, as_name=as_name)
        self.assistent = assistent

        self.tabelle = TabelleController(
            session=session,
            parent_view=self.view,
            assistent=assistent,
            root_window_controller=root_window_controller
        )
        self.view.tabelle = self.tabelle.view
        self.view.tabelle.grid()

        self.summen = SummenController(
            session=session,
            parent_view=self.view,
            assistent=assistent
        )
        self.view.summen = self.summen.view
        self.view.summen.grid()

        self.navigation = NavigationController(
            parent_controller=self,
            session=session,
            parent_view=self.view,
            controlled_areas={'tabelle': self.tabelle, 'summen': self.summen}
        )
        self.view.navigation = self.navigation.view
        self.view.navigation.grid()
        self.tabelle.nav_panel = self.navigation

        self.view.infotext = InfotextController(
            parent_controller=self,
            session=session,
            parent_view=self.view
        ).view
        self.view.infotext.grid()
        self.view.draw()
