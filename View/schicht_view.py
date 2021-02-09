import tkinter as tk

from tkcalendar import Calendar

from Helpers.combobox_dict import Combobox
from View.asn_stammdaten_view import AsnStammdatenView
from View.postadresse_view import PostadresseView
from timepicker import TimePicker


class SchichtView(tk.Toplevel):
    def __init__(self, parent_view, asn_liste, adressliste):
        super().__init__(parent_view)

        # unterframes zur optisch-logischen Einteilung
        self.asn_frame = tk.Frame(self)
        self.datetime_frame = tk.Frame(self)
        self.template_frame = tk.Frame(self.datetime_frame)
        self.add_options_frame = tk.Frame(self)
        self.add_options_checkbuttons_frame = tk.Frame(self.add_options_frame)
        self.save_buttons_frame = tk.Frame(self)

        self.asn_dropdown = Combobox(self.asn_frame,
                                     values=asn_liste,
                                     width=38,
                                     state="readonly")
        self.asn_dropdown.set("-1")

        self.asn_stammdaten_form = AsnStammdatenView(parent_view=self.asn_frame)

        self.startdatum_input = Calendar(self.datetime_frame, date_pattern='MM/dd/yyyy')
        # day=day,
        # month=month,
        # year=year)
        self.startzeit_input = TimePicker(self.datetime_frame)

        self.endzeit_input = TimePicker(self.datetime_frame)
        self.enddatum_input = Calendar(self.datetime_frame, date_pattern='MM/dd/yyyy')
        # , day=day, month=month, year=year)

        self.abweichende_adresse_beginn = PostadresseView(self.add_options_frame)
        self.abweichende_adresse_ende = PostadresseView(self.add_options_frame)

        self.abweichende_adresse_beginn_dropdown = Combobox(self.add_options_frame,
                                                            values=adressliste,
                                                            width=38,
                                                            state="readonly")
        self.abweichende_adresse_beginn_dropdown.set("-2")

        self.abweichende_adresse_ende_dropdown = Combobox(self.add_options_frame,
                                                          values=adressliste,
                                                          width=38,
                                                          state="readonly")
        self.abweichende_adresse_ende_dropdown.set("-2")

        self.ist_at = tk.IntVar()
        self.ist_pcg = tk.IntVar()
        self.ist_rb = tk.IntVar()
        self.ist_afg = tk.IntVar()
        self.ist_at_button = tk.Checkbutton(self.add_options_checkbuttons_frame,
                                            text="AT",
                                            onvalue=1, offvalue=0,
                                            variable=self.ist_at)
        self.ist_pcg_button = tk.Checkbutton(self.add_options_checkbuttons_frame,
                                             text="PCG",
                                             onvalue=1, offvalue=0,
                                            variable=self.ist_pcg)
        self.ist_rb_button = tk.Checkbutton(self.add_options_checkbuttons_frame,
                                            text="Kurzfristig (RB/BSD)",
                                            onvalue=1, offvalue=0,
                                            variable=self.ist_rb
                                            )
        self.ist_afg_button = tk.Checkbutton(self.add_options_checkbuttons_frame,
                                             text="Ausfallgeld",
                                             onvalue=1, offvalue=0,
                                            variable=self.ist_afg)

        # formbuttons
        self.save_button = tk.Button(self.save_buttons_frame, text="Daten speichern")
        self.exit_button = tk.Button(self.save_buttons_frame, text="Abbrechen")
                                     #command=self.destroy)
        self.saveandnew_button = tk.Button(self.save_buttons_frame, text="Daten speichern und neu")
                                           #command=lambda: self.action_save_neue_schicht(undneu=1))

        self.draw()

    def draw(self):

        # positionierung der Unterframes
        self.asn_frame.grid(row=0, column=0, sticky=tk.NW)
        self.datetime_frame.grid(row=0, column=1, sticky=tk.NW)
        self.template_frame.grid(row=5, column=0, sticky=tk.NW, columnspan=4)
        self.add_options_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NW)
        self.add_options_checkbuttons_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NW)
        self.save_buttons_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NE)



        # asn-frame
        asn_label = tk.Label(self.asn_frame, text='ASN auswählen')
        asn_label.grid(row=0, column=0, sticky=tk.NW)
        self.asn_dropdown.grid(row=0, column=1, sticky=tk.NE)
        self.asn_stammdaten_form.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

        # datetime-frame
        startdatum_label = tk.Label(self.datetime_frame, text='Start')
        startdatum_label.grid(row=0, column=0, sticky=tk.NW)
        self.startdatum_input.grid(row=1, column=0, sticky=tk.NW, columnspan=2)
        self.startzeit_input.grid(row=0, column=1, sticky=tk.NW)

        enddatum_label = tk.Label(self.datetime_frame, text='End')
        enddatum_label.grid(row=0, column=2, sticky=tk.NW)
        self.enddatum_input.grid(row=1, column=2, sticky=tk.NW, columnspan=2)
        self.endzeit_input.grid(row=0, column=3, sticky=tk.NW)

        # template-frame
        template_text = tk.Label(self.template_frame,
                                 text='Wenn der Assistent "Schicht-Vorlagen" hat,\n '
                                      'stehen diese hier zur Auswahl.')
        template_text.grid(row=0, column=0)

        # add-options-frame
        self.abweichende_adresse_beginn_dropdown.grid(row=0, column=0, sticky=tk.NE)
        self.abweichende_adresse_beginn.grid(row=1, column=0, sticky=tk.NW)
        self.abweichende_adresse_ende_dropdown.grid(row=0, column=1, sticky=tk.NE)
        self.abweichende_adresse_ende.grid(row=1, column=1, sticky=tk.NW)

        self.ist_at_button.grid(row=0, column=0, sticky=tk.NW)
        self.ist_pcg_button.grid(row=0, column=1, sticky=tk.NW)
        self.ist_rb_button.grid(row=0, column=2, sticky=tk.NW)
        self.ist_afg_button.grid(row=0, column=3, sticky=tk.NW)

        # save-button-frame
        self.save_button.grid(row=0, column=0)
        self.exit_button.grid(row=0, column=1)
        self.saveandnew_button.grid(row=0, column=2)

    @staticmethod
    def hide(frame: tk.Frame):
        frame.grid_remove()

    @staticmethod
    def show(frame: tk.Frame):
        frame.grid()

    def set_data(self, **kwargs):
        """
        parst alle daten ins Formular

        :param kwargs:
        :return:
        """
        if kwargs['asn']:
            self.asn_dropdown.set(kwargs['asn'])
        if kwargs['asn_stammdaten']:
            self.asn_stammdaten_form.set_data(**kwargs['asn_stammdaten'])
        if kwargs['beginn']:
            date_string = kwargs['beginn'].strftime('%m/%d/%Y')
            self.startdatum_input.parse_date(date_string)
            self.startzeit_input.hourstr.set(kwargs['beginn'].strftime('%H'))
            self.startzeit_input.minstr.set(kwargs['beginn'].strftime('%M'))
        if kwargs['ende']:
            date_string = kwargs['ende'].strftime('%m/%d/%Y')
            self.startdatum_input.parse_date(date_string)
            self.startzeit_input.hourstr.set(kwargs['ende'].strftime('%H'))
            self.startzeit_input.minstr.set(kwargs['ende'].strftime('%M'))


        # 'startdatum': self.startdatum_input.get_date(),
        # 'startzeit_stunde': self.startzeit_input.hourstr,
        # 'startzeit_minute': self.startzeit_input.minstr,
        # 'enddatum': self.startdatum_input.get_date(),
        # 'endzeit_stunde': self.startzeit_input.hourstr,
        # 'endzeit_minute': self.startzeit_input.minstr,
        # 'abweichende_adresse_beginn': self.abweichende_adresse_beginn_dropdown.get(),
        # 'abweichende_adresse_beginn_data': self.abweichende_adresse_beginn.get_data(),
        # 'abweichende_adresse_ende': self.abweichende_adresse_ende_dropdown.get(),
        # 'abweichende_adresse_ende_data': self.abweichende_adresse_ende.get_data(),
        # 'ist at': self.ist_at.get(),
        # 'ist pcg': self.ist_pcg.get(),
        # 'ist rb': self.ist_rb.get(),
        # 'ist afg': self.ist_afg.get()
    
    def get_data(self):


        return {'asn_id': self.asn_dropdown.get(),
                'asn_stammdaten': self.asn_stammdaten_form.get_data(),
                'startdatum': self.startdatum_input.get_date(),
                'startzeit_stunde': self.startzeit_input.hourstr.get(),
                'startzeit_minute': self.startzeit_input.minstr.get(),
                'enddatum': self.enddatum_input.get_date(),
                'endzeit_stunde': self.endzeit_input.hourstr.get(),
                'endzeit_minute': self.endzeit_input.minstr.get(),
                'abweichende_adresse_beginn': self.abweichende_adresse_beginn_dropdown.get(),
                'abweichende_adresse_beginn_data': self.abweichende_adresse_beginn.get_data(),
                'abweichende_adresse_ende': self.abweichende_adresse_ende_dropdown.get(),
                'abweichende_adresse_ende_data': self.abweichende_adresse_ende.get_data(),
                'ist at': self.ist_at.get(),
                'ist pcg': self.ist_pcg.get(),
                'ist rb': self.ist_rb.get(),
                'ist afg': self.ist_afg.get()}
