from View.navigation_view import NavigationView


class NavigationController:
    def __init__(self, parent_controller, session, parent_view):
        self.view = NavigationView(parent_view=parent_view)
