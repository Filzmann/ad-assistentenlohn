from datetime import datetime
from exceptions_mvc_assistenten import ItemNotStored, ItemAlreadyStored
assistenten = list()

# CREATE


def create_many(assistentenliste):
    global assistenten
    assistenten = assistentenliste


def create_one(name='', vorname='', email="keine@email.de", einstellungsdatum=datetime(1970, 1, 1, 0, 0, 0)):
    results = list(filter(lambda x: x['email'] == name, assistenten))
    if results:
        raise ItemAlreadyStored('"{}" schon gespeichert!'.format(email))
    else:
        assistenten.append({'name': name,
                            'vorname': vorname,
                            'email': email,
                            'einstellungsdatum': einstellungsdatum})

# READ


def read_assistent(email):
    global assistenten
    my_assistenten = list(filter(lambda x: x['email'] == email, assistenten))
    if my_assistenten:
        return my_assistenten[0]
    else:
        raise ItemNotStored('Assistent mit der Email-Adresse: "{}" existiert nicht'.format(email))


def read_all_assistenten():
    global assistenten
    return [assistent for assistent in assistenten]

# UPDATE


def update_item(name, vorname, email, einstellungsdatum):
    global assistenten
    idxs_items = list(
        filter(lambda i_x: i_x[1]['email'] == email, enumerate(assistenten)))
    if idxs_items:
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]
        assistenten[i] = {'name': name, 'vorname': vorname, 'email': email, 'einstellungsdatum': einstellungsdatum}
    else:
        raise ItemNotStored('Der Assistent "{}" kann leider nicht bearbeitet werden, '
                            'da er nicht vorhanden ist.'.format(email))


def delete_item(email):
    global assistenten
    idxs_items = list(
        filter(lambda i_x: i_x[1]['email'] == email, enumerate(assistenten)))
    if idxs_items:
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        del assistenten[i]
    else:
        raise ItemNotStored(
            'Kann "{}" nicht löschen, weil er nicht existiert'.format(email))