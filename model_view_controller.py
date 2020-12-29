# model_view_controller.py
import mvc_basic_backend
import exceptions_mvc_assistenten as mvc_exc


class ModelBasic(object):

    def __init__(self, application_items):
        self._item_type = 'product'
        self.create_items(application_items)

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, name, vorname, email, einstellungsdatum):
        mvc_basic_backend.create_one(name, vorname, email, einstellungsdatum)

    def create_items(self, items):
        mvc_basic_backend.create_many(items)

    def read_item(self, email):
        return mvc_basic_backend.read_item(email)

    def read_items(self):
        return mvc_basic_backend.read_items()

    def update_item(self, name, vorname, email, einstellungsdatum):
        mvc_basic_backend.update_item(name, vorname, email, einstellungsdatum)

    def delete_item(self, email):
        mvc_basic_backend.delete_item(email)