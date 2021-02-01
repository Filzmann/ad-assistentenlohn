from View.infotext_view import InfotextView


class InfotextController:
    def __init__(self, parent_controller, session, parent_view):
        self.view = InfotextView(parent_view=parent_view)
