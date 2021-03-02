import tkinter as tk
from datetime import datetime

from Helpers.timepicker import TimePicker


class SchichtTemplatesView(tk.Frame):

    def __init__(self, parent_view, schicht_templates: list = None):
        super().__init__(parent_view)
        self.tabelle = None
        self.form = tk.Frame(self)
        self.startzeit_input = TimePicker(self.form)
        self.endzeit_input = TimePicker(self.form)
        self.bezeichner_input = tk.Entry(self.form)
        self.submit_button = tk.Button(self.form, text='Vorlage hinzufügen')
        self.kill_buttons = []
        self.draw(schicht_templates)

    def draw(self, schicht_templates=None):
        if not schicht_templates:
            schicht_templates = []
        headline = tk.Label(self.form, text='Schichtvorlagen erstellen/bearbeiten')
        bezeichner = tk.Label(self.form, text='Bezeichner \n (z.B. "Früh-, Tag-, Nachtschicht")')
        von = tk.Label(self.form, text="Beginn")
        bis = tk.Label(self.form, text="Ende")
        self.form.grid(row=0, column=0, sticky=tk.NW)
        headline.grid(row=0, column=0, columnspan=2)
        bezeichner.grid(row=1, column=0, sticky=tk.NW)
        self.bezeichner_input.grid(row=1, column=1, sticky=tk.NW)
        von.grid(row=2, column=0, sticky=tk.NW)
        self.startzeit_input.grid(row=2, column=1, sticky=tk.NW)
        bis.grid(row=3, column=0, sticky=tk.NW)
        self.endzeit_input.grid(row=3, column=1, sticky=tk.NW)
        self.submit_button.grid(row=4, column=1, columnspan=2, sticky=tk.NW)

        self.tabelle = tk.Frame(self)
        self.tabelle.grid(row=0, column=1, sticky=tk.NW)
        if not schicht_templates:
            schicht_templates = []
        for child in self.tabelle.winfo_children():
            child.destroy()
        rowcounter = 0
        eintrag = tk.Label(self.tabelle, text='Deine gespeicherten Vorlagen')
        eintrag.grid(row=rowcounter, column=0)
        rowcounter += 1
        self.kill_buttons = []
        for schicht_template in schicht_templates:
            text = schicht_template['bezeichner'] + ', '
            text += schicht_template['beginn'].strftime("%H:%M") + ' - '
            text += schicht_template['ende'].strftime("%H:%M")
            eintrag = tk.Label(self.tabelle, text=text)
            eintrag.grid(row=rowcounter, column=0)

            image = "images/del.png"
            label = "Löschen"
            button = tk.Button(self.tabelle, text=label)
            button.image = tk.PhotoImage(file=image, width=16, height=16)
            button.config(image=button.image, width=16, height=16)
            button.grid(row=rowcounter, column=1)
            self.kill_buttons.append({'id': schicht_template['id'],
                                      'button': button})
            rowcounter += 1

    def get_data(self):
        startzeit = datetime(year=1, month=1, day=1,
                             hour=int(self.startzeit_input.hourstr.get()),
                             minute=int(self.startzeit_input.minstr.get()))
        endzeit = datetime(year=1, month=1, day=1,
                           hour=int(self.endzeit_input.hourstr.get()),
                           minute=int(self.endzeit_input.minstr.get()))
        return {
            "startzeit": startzeit,
            "endzeit": endzeit,
            "bezeichner": self.bezeichner_input.get()
        }
