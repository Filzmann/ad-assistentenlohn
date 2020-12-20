import tkinter as tk
import datetime
from timepicker import TimePicker
from tkcalendar import Calendar
from fenster_edit_asn import FensterEditAsn
from arbeitszeit import Schicht
from person import Adresse, ASN


class FensterNeueSchicht(tk.Toplevel):
    class AsnFrame(tk.Frame):
        class SchichtTemplates(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)
                self.parent = parent
                self.assistent = parent.assistent
                self.kuerzel = parent.parent.asn_frame.selected_asn.get()
                if self.kuerzel != 'Bitte auswählen':
                    # kuerzel = parent.parent.asn_frame.selected_asn.get()
                    if parent.parent.edit_schicht:
                        self.asn = parent.parent.edit_schicht.asn
                    else:
                        self.asn = self.assistent.get_asn_by_kuerzel(self.kuerzel)
                    self.templates = self.asn.schicht_templates
                    self.selected_template = tk.IntVar()
                    self.selected_template.set(0)
                    if not parent.parent.edit_schicht:
                        self.change_template()
                    self.draw_templates()

            def draw_templates(self):
                self.kuerzel = self.parent.parent.asn_frame.selected_asn.get()
                if self.kuerzel != 'Bitte auswählen':
                    # kuerzel = parent.parent.asn_frame.selected_asn.get()
                    asn = self.assistent.get_asn_by_kuerzel(self.kuerzel)
                    arbeitstemplates = asn.schicht_templates

                    self.selected_template = tk.IntVar()
                    self.selected_template.set(0)
                    self.change_template()

                    col = 0
                    row = 1
                    counter = 1
                    for template in arbeitstemplates:
                        text = template['bezeichner']
                        text += " von " + template["start"].strftime('%H:%M') \
                                + " bis " + template["ende"].strftime('%H:%M')
                        button = tk.Radiobutton(self, text=text,
                                                variable=self.selected_template, value=counter,
                                                command=lambda: self.change_template())
                        button.grid(row=row, column=col)
                        counter += 1
                        col += 1
                        if col == 4:
                            col = 0
                            row += 1

            def change_template(self):
                if self.kuerzel != "Bitte auswählen" and self.kuerzel != "Neuer Assistent" and \
                        self.selected_template.get() != 0:

                    asn = self.assistent.get_asn_by_kuerzel(self.kuerzel)
                    if asn.schicht_templates:
                        template_index = self.selected_template.get() - 1
                        template = asn.schicht_templates[template_index]
                        start = template["start"]
                        ende = template["ende"]
                        frame = self.parent
                        frame.startzeit_input.hourstr.set(start.strftime("%H"))
                        frame.startzeit_input.minstr.set(start.strftime("%M"))
                        frame.endzeit_input.hourstr.set(ende.strftime("%H"))
                        frame.endzeit_input.minstr.set(ende.strftime("%M"))
                        if ende < start:
                            frame.tag_nacht_reise_var.set(2)
                        else:
                            frame.tag_nacht_reise_var.set(1)

            def show(self):
                for child in self.winfo_children():
                    child.destroy()
                self.draw_templates()
                self.grid()

            def hide(self):
                self.grid_remove()

        def __init__(self, parent, edit_schicht: Schicht):
            super().__init__(parent)
            self.parent = parent
            self.edit_schicht = edit_schicht
            self.assistent = parent.assistent
            self.asn_label = tk.Label(self, text="Assistenznehmer")
            all_asn = self.assistent.get_all_asn()
            # grundsätzliche Optionen für Dropdown
            option_list = ["Bitte auswählen", "Neuer ASN", *all_asn]
            self.selected_asn = tk.StringVar()
            self.selected_asn.set(self.edit_schicht.asn.kuerzel)
            self.asn_dropdown = tk.OptionMenu(self, self.selected_asn, *option_list,
                                              command=self.change_asn)
            self.neuer_asn = FensterEditAsn.AsnEditFrame.AsnStammdatenForm(self, "Neuer ASN")

            # positionieren
            self.asn_label.grid(row=1, column=0)
            self.asn_dropdown.grid(row=1, column=1)
            self.neuer_asn.grid(row=2, column=0)
            self.neuer_asn.hide()

        def change_asn(self, selected_asn):

            if selected_asn == "Neuer ASN":
                self.neuer_asn.show()
                self.parent.schicht_calendar_frame.templates.hide()
                self.parent.save_button.grid()
                self.parent.saveandnew_button.grid()
            elif selected_asn == "Bitte auswählen":
                self.neuer_asn.hide()
                self.parent.schicht_calendar_frame.templates.hide()
                self.parent.save_button.grid_remove()
                self.parent.saveandnew_button.grid_remove()
            else:
                # self.parent.asn = self.assistent.get_asn_by_kuerzel(selected_asn)
                self.edit_schicht.asn = self.assistent.get_asn_by_kuerzel(selected_asn)
                self.neuer_asn.hide()
                self.parent.schicht_calendar_frame.templates.show()
                self.parent.schicht_add_options.destroy()
                self.parent.schicht_add_options = self.parent.SchichtAdditionalOptions(self.parent, self.edit_schicht)
                self.parent.schicht_add_options.grid(row=2, column=0, columnspan=3)
                self.parent.save_button.grid()
                self.parent.saveandnew_button.grid()

        def get_data(self):
            if self.selected_asn.get() == "Neuer ASN":
                asn = self.neuer_asn.save_stammdaten()
                self.assistent.asn_dazu(asn)
            else:
                asn = self.assistent.get_asn_by_kuerzel(self.selected_asn.get())
            self.edit_schicht.asn = asn

    class SchichtCalendarFrame(tk.Frame):
        def __init__(self, parent, edit_schicht: Schicht):
            super().__init__(parent)
            self.parent = parent
            self.edit_schicht = edit_schicht
            self.assistent = parent.assistent
            day = self.edit_schicht.beginn.day
            month = self.edit_schicht.beginn.month
            year = self.edit_schicht.beginn.year

            self.startdatum_label = tk.Label(self, text="Datum (Beginn) der Schicht")
            self.startdatum_input = Calendar(self, date_pattern='MM/dd/yyyy',
                                             day=day,
                                             month=month,
                                             year=year)
            self.startdatum_input.bind('<FocusOut>', self.enddatum_durch_startdatum)
            self.startzeit_label = tk.Label(self, text="Startzeit")
            self.startzeit_input = TimePicker(self)

            hour = self.edit_schicht.beginn.hour
            minute = self.edit_schicht.beginn.minute
            self.startzeit_input.hourstr.set(str(hour))
            self.startzeit_input.minstr.set(str(minute))
            self.startzeit_input.bind('<FocusOut>', self.nachtschicht_durch_uhrzeit)
            self.endzeit_label = tk.Label(self, text="Schichtende")
            self.endzeit_input = TimePicker(self)
            hour = self.edit_schicht.ende.hour
            minute = self.edit_schicht.ende.minute
            self.endzeit_input.hourstr.set(str(hour))
            self.endzeit_input.minstr.set(str(minute))
            self.endzeit_input.bind('<FocusOut>', self.nachtschicht_durch_uhrzeit)

            self.enddatum_label = tk.Label(self, text="Datum Ende der Schicht")
            day = self.edit_schicht.ende.day
            month = self.edit_schicht.ende.month
            year = self.edit_schicht.ende.year
            self.enddatum_input = Calendar(self, date_pattern='MM/dd/yyyy', day=day, month=month, year=year)
            self.tag_nacht_reise_var = tk.IntVar()
            self.tag_nacht_reise_var.set(1)

            b = self.edit_schicht.beginn
            e = self.edit_schicht.ende
            if datetime.date(b.year, b.month, b.day) == datetime.date(e.year, e.month, e.day):
                self.tag_nacht_reise_var.set(1)
            elif datetime.date(b.year, b.month, b.day) + datetime.timedelta(days=1) == datetime.date(e.year,
                                                                                                     e.month,
                                                                                                     e.day):
                self.tag_nacht_reise_var.set(2)
            else:
                self.tag_nacht_reise_var.set(3)
            self.anderes_enddatum_label = tk.Label(self,
                                                   text="Tagschicht, Nachtschicht\noder mehrtägig?")
            self.anderes_enddatum_input_radio1 = \
                tk.Radiobutton(self, text="Tagschicht", padx=20,
                               variable=self.tag_nacht_reise_var, value=1,
                               command=lambda: self.tag_nacht_reise(1, self.enddatum_input,
                                                                    self.enddatum_label))
            self.anderes_enddatum_input_radio2 = \
                tk.Radiobutton(self, text="Nachtschicht\n(Ende der Schicht ist am Folgetag)", padx=20,
                               variable=self.tag_nacht_reise_var, value=2,
                               command=lambda: self.tag_nacht_reise(2, self.enddatum_input,
                                                                    self.enddatum_label))
            self.anderes_enddatum_input_radio3 = \
                tk.Radiobutton(self, text="Mehrtägig/Reisebegleitung", padx=20,
                               variable=self.tag_nacht_reise_var, value=3,
                               command=lambda: self.tag_nacht_reise(3, self.enddatum_input,
                                                                    self.enddatum_label))

            self.templates = parent.asn_frame.SchichtTemplates(self)

            # positionieren
            self.startdatum_label.grid(row=0, column=0, columnspan=2, rowspan=3)
            self.startdatum_input.grid(row=1, column=0, columnspan=2, rowspan=3)
            self.enddatum_label.grid(row=0, column=2, columnspan=2, rowspan=3)
            self.enddatum_input.grid(row=1, column=2, columnspan=2, rowspan=3)
            self.startzeit_label.grid(row=4, column=0)
            self.startzeit_input.grid(row=4, column=1)
            self.endzeit_label.grid(row=4, column=2)
            self.endzeit_input.grid(row=4, column=3)
            self.anderes_enddatum_label.grid(row=0, column=2)

            self.anderes_enddatum_input_radio1.grid(row=1, column=4)
            self.anderes_enddatum_input_radio2.grid(row=2, column=4)
            self.anderes_enddatum_input_radio3.grid(row=3, column=4)

            self.templates.grid(row=5, column=0, columnspan=4)

            # self.templates.hide()

            # TODO HACK besser machen? zwingt enddatum auf invisible
            self.tag_nacht_reise(1, self.enddatum_input,
                                 self.enddatum_label)

        def nachtschicht_durch_uhrzeit(self, event):
            start = datetime.time(hour=int(self.startzeit_input.hourstr.get()),
                                  minute=int(self.startzeit_input.minstr.get()))
            ende = datetime.time(hour=int(self.endzeit_input.hourstr.get()),
                                 minute=int(self.endzeit_input.minstr.get()))

            if ende < start:
                self.tag_nacht_reise_var.set(2)
            else:
                self.tag_nacht_reise_var.set(1)

        def enddatum_durch_startdatum(self, event):
            startdatum = self.startdatum_input.get_date().split('/')
            self.enddatum_input.parse_date(self.startdatum_input.get_date())
            self.edit_schicht.ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                                       int(self.endzeit_input.hourstr.get()),
                                                       int(self.endzeit_input.minstr.get()))

        @staticmethod
        def tag_nacht_reise(value, label, button):
            if value == 3:
                label.grid()
                button.grid()
            elif value == 1 or value == 2:
                label.grid_remove()
                button.grid_remove()

        def get_data(self):
            startdatum = self.startdatum_input.get_date().split('/')
            beginn = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                       int(self.startzeit_input.hourstr.get()),
                                       int(self.startzeit_input.minstr.get()))

            # ende der Schicht bestimmen. Fälle: Tagschicht, Nachtschicht, Reise
            # todo minstring darf nicht mehr als 59 sein. kann durch ungeduldiges tippen passieren entry validieren
            if self.tag_nacht_reise_var.get() == 1:  # Tagschicht
                ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]),
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))
            elif self.tag_nacht_reise_var.get() == 2:  # Nachtschicht
                ende = datetime.datetime(int(startdatum[2]), int(startdatum[0]), int(startdatum[1]) + 1,
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))
            else:  # Reisebegleitung
                enddatum = self.enddatum_input.get_date().split('/')
                ende = datetime.datetime(int(enddatum[2]), int(enddatum[0]), int(enddatum[1]),
                                         int(self.endzeit_input.hourstr.get()),
                                         int(self.endzeit_input.minstr.get()))
            # alles wird direkt in die edit schicht geschrieben, die dann nur noch an den AS angehängt wird
            self.edit_schicht.beginn = beginn
            self.edit_schicht.ende = ende
            # return {'beginn': beginn, 'ende': ende}

    class SchichtAdditionalOptions(tk.Frame):
        class SchichtAusserHaus(tk.Frame):
            class AdressSelectOrInput(tk.Frame):
                def __init__(self, parent, selected_adresse: Adresse = None):
                    super().__init__(parent)
                    self.parent = parent
                    self.assistent = parent.assistent
                    self.selected_adresse = selected_adresse
                    self.auswahl = []
                    self.auswahl.append('Keine abweichende Adresse')
                    self.auswahl.append('Neue Adresse eintragen')
                    standardadressen = self.assistent.adressen
                    for adresse in standardadressen:
                        self.auswahl.append(adresse)
                    self.asn = self.parent.edit_schicht.asn

                    if self.asn.kuerzel != "Bitte auswählen":
                        if self.asn.adressen:
                            for adresse in self.asn.adressen:
                                self.auswahl.append(adresse)
                    self.selected = tk.StringVar()
                    if self.selected_adresse:
                        self.selected.set(self.selected_adresse)
                    else:
                        self.selected.set(self.auswahl[0])
                    dropdown = tk.OptionMenu(self, self.selected, *self.auswahl, command=self.change_dropdown)
                    dropdown.grid(row=0, column=0)

                    self.neue_adresse = tk.Frame(self)

                    self.kuerzel_label = tk.Label(self.neue_adresse, text="Bezeichner")
                    self.kuerzel_input = tk.Entry(self.neue_adresse, bd=5, width=40)
                    self.strasse_label = tk.Label(self.neue_adresse, text="Straße/Hausnummer")
                    self.strasse_input = tk.Entry(self.neue_adresse, bd=5, width=29)
                    self.hausnummer_input = tk.Entry(self.neue_adresse, bd=5, width=9)
                    self.plz_label = tk.Label(self.neue_adresse, text="Postleitzahl")
                    self.plz_input = tk.Entry(self.neue_adresse, bd=5, width=40)
                    self.stadt_label = tk.Label(self.neue_adresse, text="Stadt")
                    self.stadt_input = tk.Entry(self.neue_adresse, bd=5, width=40)

                    self.kuerzel_label.grid(row=0, column=0)
                    self.kuerzel_input.grid(row=0, column=1, columnspan=2)
                    self.strasse_label.grid(row=1, column=0)
                    self.strasse_input.grid(row=1, column=1)
                    self.hausnummer_input.grid(row=1, column=2)
                    self.plz_label.grid(row=2, column=0)
                    self.plz_input.grid(row=2, column=1, columnspan=2)
                    self.stadt_label.grid(row=3, column=0)
                    self.stadt_input.grid(row=3, column=1, columnspan=2)
                    self.neue_adresse.grid(row=1, column=0)
                    self.neue_adresse.grid_remove()

                def change_dropdown(self, selected):
                    if selected == 'Neue Adresse eintragen':
                        self.neue_adresse.grid()
                    else:
                        self.neue_adresse.grid_remove()

                def get_data(self):
                    if self.selected.get() == "Keine abweichende Adresse":
                        return []
                    elif self.selected.get() == "Neue Adresse eintragen":
                        adresse = Adresse(kuerzel=self.kuerzel_input.get(),
                                          strasse=self.strasse_input.get(),
                                          hnr=self.hausnummer_input.get(),
                                          plz=self.plz_input.get(),
                                          stadt=self.stadt_input.get())
                        if adresse not in self.parent.edit_schicht.asn.adressen:
                            self.parent.edit_schicht.asn.adressen.append(adresse)
                        return adresse
                    else:
                        asn_adresse = self.asn.get_adresse_by_kuerzel(self.selected.get())
                        if asn_adresse:
                            return asn_adresse
                        else:
                            as_adresse = self.assistent.get_adresse_by_kuerzel(self.selected.get())
                            return as_adresse

            def __init__(self, parent, edit_schicht: Schicht = 0):
                super().__init__(parent)
                self.parent = parent
                self.edit_schicht = edit_schicht
                self.assistent = parent.assistent

                self.alternative_adresse_beginn_label = tk.Label(self,
                                                                 text="Beginn der Schicht außer Haus")
                adresse_beginn = self.edit_schicht.beginn_andere_adresse
                self.alternative_adresse_beginn_input = \
                    self.AdressSelectOrInput(self, adresse_beginn)
                adresse_ende = self.edit_schicht.ende_andere_adresse
                self.alternative_adresse_ende_label = tk.Label(self,
                                                               text="Ende der Schicht außer Haus")
                self.alternative_adresse_ende_input = \
                    self.AdressSelectOrInput(self, adresse_ende)

                self.alternative_adresse_beginn_label.grid(row=0, column=0)
                self.alternative_adresse_beginn_input.grid(row=0, column=1)
                self.alternative_adresse_ende_label.grid(row=1, column=0)
                self.alternative_adresse_ende_input.grid(row=1, column=1)

            def get_data(self):
                self.edit_schicht.beginn_andere_adresse = self.alternative_adresse_beginn_input.get_data()
                self.edit_schicht.ende_andere_adresse = self.alternative_adresse_ende_input.get_data()

        def __init__(self, parent, edit_schicht: Schicht = 0):
            super().__init__(parent)
            self.parent = parent
            self.edit_schicht = edit_schicht
            self.assistent = parent.assistent
            self.ist_at = tk.IntVar()
            self.ist_pcg = tk.IntVar()
            self.ist_rb = tk.IntVar()
            self.ist_afg = tk.IntVar()

            if self.edit_schicht.ist_assistententreffen:
                self.ist_at.set(1)
            if self.edit_schicht.ist_ausfallgeld:
                self.ist_afg.set(1)
            if self.edit_schicht.ist_kurzfristig:
                self.ist_rb.set(1)
            if self.edit_schicht.ist_pcg:
                self.ist_pcg.set(1)

            self.ist_at_button = tk.Checkbutton(self, text="AT", variable=self.ist_at, onvalue=1, offvalue=0)
            self.ist_pcg_button = tk.Checkbutton(self, text="PCG", variable=self.ist_pcg, onvalue=1, offvalue=0)
            self.ist_rb_button = tk.Checkbutton(self, text="Kurzfristig (RB/BSD)", variable=self.ist_rb, onvalue=1,
                                                offvalue=0)
            self.ist_afg_button = tk.Checkbutton(self, text="Ausfallgeld", variable=self.ist_afg, onvalue=1, offvalue=0)
            self.ausser_haus = self.SchichtAusserHaus(parent=self, edit_schicht=self.edit_schicht)

            # positionieren
            self.ist_at_button.grid(row=0, column=0)
            self.ist_pcg_button.grid(row=0, column=1)
            self.ist_rb_button.grid(row=0, column=2)
            self.ist_afg_button.grid(row=0, column=3)

            self.ausser_haus.grid(row=1, column=0, columnspan=4)

        def get_data(self):
            self.ausser_haus.get_data()
            self.edit_schicht.ist_assistententreffen = self.ist_at.get()
            self.edit_schicht.ist_pcg = self.ist_pcg.get()
            self.edit_schicht.ist_kurzfristig = self.ist_rb.get()
            self.edit_schicht.ist_ausfallgeld = self.ist_afg.get()

    def __init__(self, parent, assistent, edit_schicht: Schicht = None, datum: datetime.datetime = None):
        super().__init__(parent)
        self.parent = parent
        self.assistent = assistent
        # wenn neue Schicht, dann leere Schicht vordefinieren, die beim Speichern nur noch dem AS hinzugefügt wird
        self.neu = 0
        if not edit_schicht:
            self.neu = 1
            empty_asn = ASN(name='', vorname='', kuerzel='Bitte auswählen')
            if datum:
                init_date = datum
            else:
                init_date = self.assistent.letzte_eingetragene_schicht.beginn

            self.edit_schicht = Schicht(beginn=init_date,
                                        ende=init_date + datetime.timedelta(hours=1),
                                        asn=empty_asn,
                                        assistent=assistent)
        else:
            # falls die gewähle Schicht Teilschicht eines Splits ist.
            if edit_schicht.original_schicht != 'root':
                self.edit_schicht = edit_schicht.original_schicht
            else:
                self.edit_schicht = edit_schicht

        self.asn_frame = self.AsnFrame(self, self.edit_schicht)
        self.schicht_calendar_frame = self.SchichtCalendarFrame(self, self.edit_schicht)
        self.schicht_add_options = self.SchichtAdditionalOptions(self, self.edit_schicht)

        # positionieren
        self.asn_frame.grid(row=0, column=0, columnspan=3)
        self.schicht_calendar_frame.grid(row=1, column=0, columnspan=3)
        self.schicht_add_options.grid(row=2, column=0, columnspan=3)

        self.save_button = tk.Button(self, text="Daten speichern",
                                     command=self.action_save_neue_schicht)
        self.exit_button = tk.Button(self, text="Abbrechen",
                                     command=self.destroy)
        self.saveandnew_button = tk.Button(self, text="Daten speichern und neu",
                                           command=lambda: self.action_save_neue_schicht(undneu=1))

        #    self.templates.grid(row=2, column=0, columnspan=4)

        self.save_button.grid(row=3, column=0)
        self.exit_button.grid(row=3, column=1)
        self.saveandnew_button.grid(row=3, column=2)
        self.saveandnew_button.grid_remove()
        if not edit_schicht:
            self.save_button.grid_remove()

    def action_save_neue_schicht(self, undneu=0):
        self.schicht_calendar_frame.get_data()
        self.asn_frame.get_data()
        self.schicht_add_options.get_data()
        self.edit_schicht.calculate()
        # Schicht erstellen und zum Assistenten stopfen
        if self.neu:
            self.assistent.schicht_dazu(self.edit_schicht)
        self.assistent.letzte_eingetragene_schicht = self.edit_schicht
        assistent = self.assistent.save_to_file()
        # TODO quick'n'dirty Hack korrigieren
        if self.neu:
            self.parent.fenster.redraw(assistent)
        else:
            self.parent.parent.redraw(assistent)
        self.destroy()
        if undneu == 1:
            FensterNeueSchicht(self.parent, assistent=assistent)
