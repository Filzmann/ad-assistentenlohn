import tkinter as tk
from datetime import datetime

from Helpers.timepicker import TimePicker


class FesteSchichtenView(tk.Frame):

    def __init__(self, parent_view, feste_schichten: list = None):
        super().__init__(parent_view)
        self.tabelle = None
        self.selected_day = tk.StringVar()
        self.form = tk.Frame(self)
        self.startzeit_input = TimePicker(self.form)
        self.endzeit_input = TimePicker(self.form)

        wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
                      'Auswählen']
        self.selected_day.set(wochentage[7])
        self.form_wochentage_dropdown = tk.OptionMenu(self.form, self.selected_day, *wochentage)
        self.submit_button = tk.Button(self.form, text='feste Schicht hinzufügen')
        self.kill_buttons = []
        self.draw(feste_schichten)

    def draw(self, feste_schichten=None):
        if not feste_schichten:
            feste_schichten = []
        headline = tk.Label(self.form, text='Feste Schichten erstellen/bearbeiten')
        jeden = tk.Label(self.form, text="Jeden")
        von = tk.Label(self.form, text="Von")
        bis = tk.Label(self.form, text="bis")
        self.form.grid(row=0, column=0, sticky=tk.NW)
        headline.grid(row=0, column=0, columnspan=2, sticky=tk.NW)
        jeden.grid(row=1, column=0, sticky=tk.NW)
        self.form_wochentage_dropdown.grid(row=1, column=1, sticky=tk.NW)
        von.grid(row=2, column=0, sticky=tk.NW)
        self.startzeit_input.grid(row=2, column=1, sticky=tk.NW)
        bis.grid(row=3, column=0, sticky=tk.NW)
        self.endzeit_input.grid(row=3, column=1, sticky=tk.NW)
        self.submit_button.grid(row=4, column=1, columnspan=2, sticky=tk.NW)

        self.tabelle = tk.Frame(self)
        self.tabelle.grid(row=0, column=1, sticky=tk.NW)
        if not feste_schichten:
            feste_schichten = []
        for child in self.tabelle.winfo_children():
            child.destroy()
        rowcounter = 0
        eintrag = tk.Label(self.tabelle, text='Deine festen Schichten\nin diesem Einsatz')
        eintrag.grid(row=rowcounter, column=0)
        rowcounter += 1
        self.kill_buttons = []
        for feste_schicht in feste_schichten:
            text = feste_schicht['wochentag'] + ', '
            text += feste_schicht['beginn'].strftime("%H:%M") + ' - '
            text += feste_schicht['ende'].strftime("%H:%M")
            eintrag = tk.Label(self.tabelle, text=text)
            eintrag.grid(row=rowcounter, column=0, sticky=tk.NW)

            image = "images/del.png"
            label = "Löschen"
            button = tk.Button(self.tabelle, text=label)
            button.image = tk.PhotoImage(file=image, width=16, height=16)
            button.config(image=button.image, width=16, height=16)
            button.grid(row=rowcounter, column=1, sticky=tk.NW)
            self.kill_buttons.append({'id': feste_schicht['id'],
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
            "selected_day": self.selected_day.get()
        }
