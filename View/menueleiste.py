import tkinter as tk
from tkinter import messagebox as messagebox

from Controller.arbeitsunfaehigkeit_controller import AUController
from Controller.asn_edit_controller import AsnEditController
from Controller.assistent_controller import AssistentController
from Controller.kilometergeld_controller import KilometergeldController
from Controller.schicht_controller import SchichtController
from Controller.urlaub_controller import UrlaubController
from Controller.verpflegungsmehraufwand_controller import VerpflegungsmehraufwandController


class Menuleiste(tk.Menu):
    def __init__(self, parent_view, assistent, parent_controller, session, nav_panel=None):
        tk.Menu.__init__(self, parent_view)
        # Menü Datei und Help erstellen
        datei_menu = tk.Menu(self, tearoff=0)
        datei_menu.add_separator()  # Fügt eine Trennlinie hinzu
        datei_menu.add_command(label="Exit", command=parent_view.quit)

        eintragen_menu = tk.Menu(self, tearoff=0)
        eintragen_menu.add_command(label="Schicht eintragen",
                                   command=lambda: SchichtController(
                                       parent_controller=parent_controller,
                                       session=session,
                                       assistent=assistent,
                                       nav_panel=nav_panel))
        eintragen_menu.add_command(label="Urlaub eintragen",
                                   command=lambda: UrlaubController(parent_controller,
                                                                    session=session,
                                                                    assistent=assistent,
                                                                    nav_panel=nav_panel))
        eintragen_menu.add_command(label="AU/krank eintragen",
                                   command=lambda: AUController(parent_controller,
                                                                session=session,
                                                                assistent=assistent,
                                                                nav_panel=nav_panel))

        bearbeiten_menu = tk.Menu(self, tearoff=0)
        bearbeiten_menu.add_command(label="ASN bearbeiten",
                                    command=lambda: AsnEditController(parent_controller=parent_controller,
                                                                      assistent=assistent,
                                                                      session=session))
        bearbeiten_menu.add_command(label="Assistent bearbeiten",
                                    command=lambda: AssistentController(parent_controller=parent_controller,
                                                                        assistent=assistent,
                                                                        session=session))

        taxes_menu = tk.Menu(self, tearoff=0)
        taxes_menu.add_command(label="Verpflegungsmehraufwand",
                               command=lambda: VerpflegungsmehraufwandController(
                                   parent_controller=parent_controller,
                                   assistent=assistent,
                                   session=session))
        taxes_menu.add_command(label="Reisekosten/KM-Geld",
                               command=lambda: KilometergeldController(
                                   parent_controller=parent_controller,
                                   assistent=assistent,
                                   session=session))

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="Info!", command=self.action_get_info_dialog)

        self.add_cascade(label="Datei", menu=datei_menu)
        self.add_cascade(label="Eintragen", menu=eintragen_menu)
        self.add_cascade(label="Bearbeiten", menu=bearbeiten_menu)
        self.add_cascade(label="Einkommenssteuer", menu=taxes_menu)
        self.add_cascade(label="Help", menu=help_menu)

    @staticmethod
    def action_get_info_dialog():
        m_text = "\
    ************************\n\
    Autor: Simon Beyer\n\
    Date: 16.11.2020\n\
    Version: 0.01\n\
    ************************"
        messagebox.showinfo(message=m_text, title="Infos")
