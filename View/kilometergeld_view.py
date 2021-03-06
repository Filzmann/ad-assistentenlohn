import tkinter as tk


from Helpers.combobox_dict import Combobox


class KilometergeldView(tk.Toplevel):
    def __init__(self, parent_view, **kwargs):
        super().__init__(parent_view)
        self.parent = parent_view

        if 'jahrarray' in kwargs:
            self.jahr_dropdown = Combobox(self, values=kwargs['jahrarray'], width=5, state="readonly")
            self.changebutton = tk.Button(self, text='Go!')
        text = ''
        for zeile in kwargs['data'].values():
            text += str(zeile['count']) + ' Fahrten zwischen '
            text += zeile['adresse_1'].strasse + ', ' + str(zeile['adresse_1'].plz) + ' ' + zeile['adresse_1'].stadt
            text += ' und '
            text += zeile['adresse_2'].strasse + ', ' + str(zeile['adresse_2'].plz) + ' ' + zeile['adresse_2'].stadt
            text += ' => ' + str(zeile['count']) + ' * ' + "{:,.2f}".format(zeile['entfernung']) \
                    + 'km ' + ' * 0,30€ = ' + "{:,.2f}€".format(zeile['kmgeld'])
            text += '\n'

        self.textfeld = tk.Text(self, width=130, height=50)
        # self.ys = ttk.Scrollbar(self, orient='vertical', command=self.textfeld.yview)
        # self.xs = ttk.Scrollbar(self, orient='horizontal', command=self.textfeld.xview)
        # self.textfeld['yscrollcommand'] = self.ys.set
        # self.textfeld['xscrollcommand'] = self.xs.set
        self.textfeld.insert('1.0', text)

        self.draw()

    def draw(self):
        # ins Fenster packen
        headline = tk.Label(self, text="Reisekosten/Kilometergeld")
        headline.grid(row=0, column=0, columnspan=2)

        if hasattr(self, 'jahr_dropdown'):
            self.jahr_dropdown.grid(row=0, column=5)
            self.changebutton.grid(row=0, column=6)

        self.textfeld.grid(row=1, column=0, columnspan=3)
        # self.xs.grid(column=0, row=1, sticky='we')
        # self.ys.grid(column=1, row=0, sticky='ns')
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

    def set_data(self, **kwargs):
        pass

    def get_data(self):
        pass
