from View.summen_view import SummenView


class SummenController:
    def __init__(self, parent_controller, session_maker, parent_view):
        self.view = SummenView(parent_view=parent_view)