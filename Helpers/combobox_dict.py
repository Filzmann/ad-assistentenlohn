from tkinter import ttk


class Combobox(ttk.Combobox):
    """erzeugt eine Combobox, die ein dict als optionlist annimmt.
    in der Liste werden die Values angezeigt und per get ausgegeben werden die keys (Beispiel id für db)
    Achtung: die Values müssen unique sein.
    """

    def __init__(self, master=None, cnf=None, **options):

        if not cnf:
            cnf = {}
        self.dict = None

        # get dictionary from options and put list of keys
        if 'values' in options:
            if isinstance(options.get('values'), dict):
                self.dict = options.get('values')
                options['values'] = sorted(self.dict.values())

        # combobox constructor with list of keys
        ttk.Combobox.__init__(self, master=master, **options)

    # overwrite `get()` to return `key` instead of `value`
    def get(self):
        if self.dict:
            return self.get_key()
        else:
            return ttk.Combobox.get(self)

    def set(self, key):
        """
        :param key: key / id
        :return:
        """

        value = self.dict[key]
        ttk.Combobox.set(self, value=value)

    def get_key(self):
        val = ttk.Combobox.get(self)
        for key, value in self.dict.items():
            if val == str(value):
                return key
        return False

    def get_value(self):
        return ttk.Combobox.get(self)
