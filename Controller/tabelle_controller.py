from View.tabelle_view import TabelleView


class TabelleController:
    def __init__(self, parent_controller, session_maker, parent_view):
        self.view = TabelleView(parent_view=parent_view)
