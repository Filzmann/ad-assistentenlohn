import tkinter as tk
import datetime
from timepicker import TimePicker
from person import ASN, EB


class FensterEditAsn(tk.Toplevel):
    class AsnAuswahllisteFrame(tk.Frame):
        def __init__(self, parent, kuerzel=''):
            assistent = parent.assistent
            super().__init__(parent)
            self.parent = parent
            self.asn_options = list(assistent.get_all_asn().keys())
            self.selected_asn = tk.StringVar()

            self.asn_options.insert(0, "Neuer ASN")
            if kuerzel:
                self.selected_asn.set(kuerzel)
            else:
                self.selected_asn.set("Neuer ASN")

            for kuerzel in self.asn_options:
                button = tk.Radiobutton(self, text=kuerzel, padx=20,
                                        variable=self.selected_asn, value=kuerzel,
                                        command=self.choose_asn)
                button.pack()
            self.choose_asn()

        def choose_asn(self):
            kuerzelAusgewaehlt = self.selected_asn.get()
            if self.parent.editframe:
                self.parent.editframe.destroy()
            self.parent.editframe = self.parent.AsnEditFrame(self.parent, kuerzelAusgewaehlt)
            self.parent.editframe.grid(row=0, column=1)

    class AsnEditFrame(tk.Frame):
        class FesteSchichtForm(tk.Frame):
            class FesteSchichtTabelle(tk.Frame):

                def __init__(self, parent, asn):
                    super().__init__(parent)
                    self.assistent = parent.assistent
                    self.asn = asn
                    self.draw()

                def draw(self):
                    for child in self.winfo_children():
                        child.destroy()
                    rowcounter = 0
                    eintrag = tk.Label(self, text='Deine festen Schichten\nin diesem Einsatz')
                    eintrag.grid(row=rowcounter, column=0, columnspan=2)
                    rowcounter += 1
                    for feste_schicht in self.assistent.festeSchichten:
                        if feste_schicht['asn'] == self.asn.kuerzel:
                            text = feste_schicht['wochentag'] + ', '
                            text += feste_schicht['start'].strftime("%H:%M") + ' - '
                            text += feste_schicht['ende'].strftime("%H:%M")
                            eintrag = tk.Label(self, text=text)
                            eintrag.grid(row=rowcounter, column=0)

                            image = "images/del.png"
                            label = "Löschen"
                            button = tk.Button(self, text=label,
                                               command=lambda: self.kill_feste_schicht(feste_schicht))
                            button.image = tk.PhotoImage(file=image, width=16, height=16)
                            button.config(image=button.image, width=16, height=16)
                            button.grid(row=rowcounter, column=1)
                            rowcounter += 1

                def kill_feste_schicht(self, feste_schicht):
                    self.assistent.festeSchichten.remove(feste_schicht)
                    self.draw()

            def __init__(self, parent, asn):
                super().__init__(parent)
                self.asn = asn
                self.assistent = parent.assistent
                headline = tk.Label(self, text='Feste Schichten erstellen/bearbeiten')
                headline.grid(row=0, column=0, columnspan=3)
                jeden = tk.Label(self, text="Jeden")
                jeden.grid(row=1, column=0)
                wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
                              'Auswählen']
                self.gewaehlter_tag = tk.StringVar()
                self.gewaehlter_tag.set(wochentage[7])
                form_wochentage_dropdown = tk.OptionMenu(self, self.gewaehlter_tag, *wochentage)
                form_wochentage_dropdown.grid(row=1, column=1)
                von = tk.Label(self, text="Von")
                von.grid(row=2, column=0)
                self.startzeit_input = TimePicker(self)
                self.startzeit_input.grid(row=2, column=1)
                bis = tk.Label(self, text="bis")
                bis.grid(row=3, column=0)
                self.endzeit_input = TimePicker(self)
                self.endzeit_input.grid(row=3, column=1)
                self.schichtliste = self.FesteSchichtTabelle(self, asn)
                self.schichtliste.grid(row=1, column=3, rowspan=3)
                submit_button = tk.Button(self, text='feste Schicht hinzufügen',
                                          command=self.save_feste_schicht)
                submit_button.grid(row=4, column=1, columnspan=2)

            def save_feste_schicht(self):
                if self.gewaehlter_tag.get() != 'Auswählen':
                    wochentag = self.gewaehlter_tag.get()
                    startzeit_stunde = int(self.startzeit_input.hourstr.get())
                    startzeit_minute = int(self.startzeit_input.minstr.get())
                    endzeit_stunde = int(self.endzeit_input.hourstr.get())
                    endzeit_minute = int(self.endzeit_input.minstr.get())
                    s_feste_schicht = {'asn': self.asn.kuerzel,
                                       'wochentag': wochentag,
                                       'start': datetime.time(startzeit_stunde, startzeit_minute, 0),
                                       'ende': datetime.time(endzeit_stunde, endzeit_minute, 0)}
                    self.assistent.festeSchichten.append(s_feste_schicht)
                    self.schichtliste.draw()
                    self.assistent.save_to_file()

        class SchichtTemplateForm(tk.Frame):
            class TemplateTabelle(tk.Frame):

                def __init__(self, parent, asn):
                    self.assistent = parent.assistent
                    super().__init__(parent)
                    self.asn = asn
                    self.draw()

                def draw(self):
                    for child in self.winfo_children():
                        child.destroy()
                    rowcounter = 0
                    eintrag = tk.Label(self, text='Deine Vorlagen\nfür diesem Einsatz')
                    eintrag.grid(row=rowcounter, column=0)
                    rowcounter += 1
                    for template in self.asn.schicht_templates:
                        text = template['bezeichner'] + ': '
                        text += template['start'].strftime("%H:%M") + ' - '
                        text += template['ende'].strftime("%H:%M")
                        eintrag = tk.Label(self, text=text)
                        eintrag.grid(row=rowcounter, column=0)

                        image = "images/del.png"
                        label = "Löschen"
                        button = tk.Button(self, text=label,
                                           command=lambda: self.kill_template(template))
                        button.image = tk.PhotoImage(file=image, width=16, height=16)
                        button.config(image=button.image, width=16, height=16)
                        button.grid(row=rowcounter, column=1)

                        rowcounter += 1

                def kill_template(self, template):
                    self.asn.schicht_templates.remove(template)
                    self.draw()

            def __init__(self, parent, asn):
                self.asn = asn
                super().__init__(parent)
                self.assistent = parent.assistent
                headline = tk.Label(self, text='Schichtvorlagen erstellen/bearbeiten')
                headline.grid(row=0, column=0, columnspan=2)
                bezeichner = tk.Label(self, text="Bezeichner (z.B. \"Frühschicht\")")
                bezeichner.grid(row=1, column=0)
                self.bezeichner = tk.Entry(self)
                self.bezeichner.grid(row=1, column=1)
                von = tk.Label(self, text="Von")
                von.grid(row=2, column=0)
                self.startzeit_input = TimePicker(self)
                self.startzeit_input.grid(row=2, column=1)
                bis = tk.Label(self, text="bis")
                bis.grid(row=3, column=0)
                self.endzeit_input = TimePicker(self)
                self.endzeit_input.grid(row=3, column=1)
                self.templateliste = self.TemplateTabelle(self, asn=asn)
                self.templateliste.grid(row=1, column=3, rowspan=3)

                submit_button = tk.Button(self, text='Schichtvorlage hinzufügen',
                                          command=self.save_schicht_template)
                submit_button.grid(row=4, column=1, columnspan=2)

            def save_schicht_template(self):
                bezeichner = self.bezeichner.get()
                startzeit_stunde = int(self.startzeit_input.hourstr.get())
                startzeit_minute = int(self.startzeit_input.minstr.get())
                endzeit_stunde = int(self.endzeit_input.hourstr.get())
                endzeit_minute = int(self.endzeit_input.minstr.get())
                s_feste_schicht = {'bezeichner': bezeichner,
                                   'start': datetime.time(startzeit_stunde, startzeit_minute, 0),
                                   'ende': datetime.time(endzeit_stunde, endzeit_minute, 0)}
                self.asn.schicht_templates.append(s_feste_schicht)
                self.templateliste.draw()
                # zeichne_feste_schichten_form(self)

        class AsnStammdatenForm(tk.Frame):
            def __init__(self, parent, asn):
                self.asn = asn
                super().__init__(parent)
                kuerzel_label = tk.Label(self, text="Kürzel")
                self.kuerzel_input = tk.Entry(self, bd=5, width=40)
                vorname_label = tk.Label(self, text="Vorname")
                self.vorname_input = tk.Entry(self, bd=5, width=40)
                nachname_label = tk.Label(self, text="Nachname")
                self.nachname_input = tk.Entry(self, bd=5, width=40)
                strasse_label = tk.Label(self, text="Straße/Hausnummer")
                self.strasse_input = tk.Entry(self, bd=5, width=29)
                self.hausnummer_input = tk.Entry(self, bd=5, width=9)
                plz_label = tk.Label(self, text="Postleitzahl")
                self.plz_input = tk.Entry(self, bd=5, width=40)
                stadt_label = tk.Label(self, text="Stadt")
                self.stadt_input = tk.Entry(self, bd=5, width=40)
                buero_label = tk.Label(self, text="Zuständiges Einsatzbüro")
                # TODO in Klassen überführen
                option_list = ['Bitte auswählen', 'Nordost', 'West', 'Süd']
                self.selected_buero = tk.StringVar()
                self.selected_buero.set(option_list[0])
                self.buero_dropdown = tk.OptionMenu(self, self.selected_buero, *option_list)
                if self.asn != 'Neuer ASN':
                    self.kuerzel_input.insert(0, self.asn.kuerzel)
                    if self.asn.kuerzel != '':
                        self.kuerzel_input.config(state='disabled')
                    self.vorname_input.insert(0, self.asn.vorname)
                    self.nachname_input.insert(0, self.asn.name)
                    self.strasse_input.insert(0, self.asn.strasse)
                    self.hausnummer_input.insert(0, self.asn.hausnummer)
                    self.plz_input.insert(0, self.asn.plz)
                    self.stadt_input.insert(0, self.asn.stadt)

                # positionieren
                kuerzel_label.grid(row=0, column=0)
                self.kuerzel_input.grid(row=0, column=1, columnspan=2)
                vorname_label.grid(row=1, column=0)
                self.vorname_input.grid(row=1, column=1, columnspan=2)
                nachname_label.grid(row=2, column=0)
                self.nachname_input.grid(row=2, column=1, columnspan=2)
                strasse_label.grid(row=3, column=0)
                self.strasse_input.grid(row=3, column=1)
                self.hausnummer_input.grid(row=3, column=2)
                plz_label.grid(row=4, column=0)
                self.plz_input.grid(row=4, column=1, columnspan=2)
                stadt_label.grid(row=5, column=0)
                self.stadt_input.grid(row=5, column=1, columnspan=2)
                buero_label.grid(row=6, column=0)
                self.buero_dropdown.grid(row=6, column=1)

            def show(self):
                self.grid()

            def hide(self):
                self.grid_remove()

            def save_stammdaten(self):
                # Stammdaten speichern
                vname = self.vorname_input.get()
                name = self.nachname_input.get()
                strasse = self.strasse_input.get()
                hnr = self.hausnummer_input.get()
                plz = self.plz_input.get()
                stadt = self.stadt_input.get()
                neues_kuerzel = self.kuerzel_input.get()

                if self.asn == 'Neuer ASN':
                    asn = ASN(name, vname, neues_kuerzel, strasse, hnr, plz, stadt)
                else:
                    asn = self.asn
                    asn.vorname = vname
                    asn.name = name
                    asn.strasse = strasse
                    asn.hausnummer = hnr
                    asn.stadt = stadt
                    asn.plz = plz
                    asn.kuerzel = neues_kuerzel

                asn.buero = self.selected_buero.get()
                return asn

        class EbPfkEditForm(tk.Frame):
            def __init__(self, parent, asn, eb_oder_pfk):
                self.asn = asn
                self.parent = parent
                super().__init__(parent)
                assistent = parent.assistent
                first, text, liste, select_what = '', '', [], []

                self.selected = tk.StringVar()
                if eb_oder_pfk == 'eb':
                    text = "Einsatzbegleitung"
                    liste = assistent.eb_liste
                    first = "Neue EB"
                    select_what = asn.eb
                    if self.asn.eb:
                        if asn.eb.name == '' and asn.eb.vorname == '':
                            self.selected.set(first)
                        else:
                            self.selected.set(select_what)
                    else:
                        self.selected.set(first)
                elif eb_oder_pfk == 'pfk':
                    text = "Pflegefachkraft"
                    liste = assistent.pfk_liste
                    first = "Neue PFK"
                    select_what = asn.pfk
                    if self.asn.pfk:
                        if self.asn.pfk.name == '' and self.asn.pfk.vorname == '':
                            self.selected.set(first)
                        else:
                            self.selected.set(select_what)
                    else:
                        self.selected.set(first)
                headline = tk.Label(self, text=text)
                option_list = [first, *liste]

                self.eb_dropdown = tk.OptionMenu(self, self.selected, *option_list, command=self.change_person)

                vorname_label = tk.Label(self, text="Vorname")
                self.vorname_input = tk.Entry(self, bd=5, width=40)
                nachname_label = tk.Label(self, text="Nachname")
                self.nachname_input = tk.Entry(self, bd=5, width=40)
                email_label = tk.Label(self, text="Email")
                self.email_input = tk.Entry(self, bd=5, width=40)

                if select_what:
                    self.vorname_input.insert(0, select_what.vorname)
                    self.nachname_input.insert(0, select_what.name)
                    self.email_input.insert(0, select_what.email)

                headline.grid(row=0, column=0)
                self.eb_dropdown.grid(row=0, column=1)
                vorname_label.grid(row=1, column=0)
                self.vorname_input.grid(row=1, column=1)
                nachname_label.grid(row=2, column=0)
                self.nachname_input.grid(row=2, column=1)
                email_label.grid(row=3, column=0)
                self.email_input.grid(row=3, column=1)

            def change_person(self, person):
                self.vorname_input.delete(0, 'end')
                self.nachname_input.delete(0, 'end')
                self.email_input.delete(0, 'end')
                if person != 'Neue EB' and person != 'Neue PFK':
                    self.vorname_input.insert(0, person.vorname)
                    self.nachname_input.insert(0, person.name)
                    self.email_input.insert(0, person.email)

            def save_person(self, eb_oder_pfk='eb'):
                assistent = self.parent.assistent
                if eb_oder_pfk == 'eb':
                    person = self.asn.eb
                else:
                    person = self.asn.pfk

                if self.nachname_input.get() != '' \
                        or self.vorname_input.get() != '' \
                        or self.email_input.get() != '':

                    if eb_oder_pfk == 'eb':
                        abgleich = assistent.get_eb_by_string(self.selected.get())
                    else:
                        abgleich = assistent.get_pfk_by_string(self.selected.get())

                    if self.selected.get() == "Neue EB" or self.selected.get == "Neue PFK":
                        person = EB(name=self.nachname_input.get(),
                                    vorname=self.vorname_input.get(),
                                    email=self.email_input.get())
                    elif abgleich == person:
                        # aktuelle person bearbeiten

                        person.name = self.nachname_input.get()
                        person.vorname = self.vorname_input.get()
                        person.email = self.email_input.get()
                    else:
                        person = assistent.get_eb_by_string(self.selected.get())

                    if eb_oder_pfk == 'eb':
                        self.asn.eb = person
                    else:
                        self.asn.pfk = person
                    if person not in assistent.eb_liste and eb_oder_pfk == 'eb':
                        assistent.eb_liste.append(person)
                    elif person not in assistent.pfk_liste and eb_oder_pfk == 'pfk':
                        assistent.pfk_liste.append(person)

        def __init__(self, parent, kuerzel):

            super().__init__(parent)
            self.parent = parent
            self.assistent = parent.assistent
            if kuerzel == 'Neuer ASN':
                self.asn = ASN('', '', '', '', '', '', 'Berlin')
            else:
                self.asn = self.assistent.get_asn_by_kuerzel(kuerzel)

            self.stammdatenframe = self.AsnStammdatenForm(self, self.asn)
            self.stammdatenframe.grid(row=0, column=0, rowspan=2)
            self.eb_frame = self.EbPfkEditForm(self, self.asn, 'eb')
            self.eb_frame.grid(row=0, column=1)

            # todo fix PFK
            # self.pfk_frame = self.EbPfkEditForm(self, self.asn, 'pfk')
            # self.pfk_frame.grid(row=1, column=1)

            self.feste_schichten_frame = self.FesteSchichtForm(self, self.asn)
            self.feste_schichten_frame.grid(row=2, column=0)
            self.schicht_templates_frame = self.SchichtTemplateForm(self, self.asn)
            self.schicht_templates_frame.grid(row=2, column=1)

            save_button = tk.Button(self, text="Daten speichern", command=lambda: self.save_asn_edit_form())
            exit_button = tk.Button(self, text="Fenster schließen", command=lambda: self.parent.destroy())
            save_button.grid(row=5, column=1)
            exit_button.grid(row=5, column=0)

        def save_asn_edit_form(self):

            asn = self.stammdatenframe.save_stammdaten()
            self.eb_frame.save_person(eb_oder_pfk='eb')
            # self.pfk_frame.save_person(eb_oder_pfk='pfk')
            self.assistent.asn[asn.kuerzel] = asn
            self.assistent.save_to_file()
            self.parent.destroy()
            FensterEditAsn(self.parent.parent, self.assistent, kuerzel=asn.kuerzel)

    def __init__(self, parent, assistent, kuerzel=''):

        super().__init__(parent)
        self.assistent = assistent
        self.parent = parent
        self.editframe = self.AsnEditFrame(self, "Neuer ASN")
        self.auswahlframe = self.AsnAuswahllisteFrame(self, kuerzel)
        self.auswahlframe.grid(row=0, column=0)
        self.editframe.grid(row=0, column=1)
