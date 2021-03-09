import tkinter as tk


class InfotextView(tk.Frame):
    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.config(
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
            bd=0)
        infotext = "Achtung, \n" \
                   "diese Version des Programmes ist noch absolut alpha, sprich \n" \
                   "eine Testversion. Ich verbreite diese, damit sie auf Herz und \n" \
                   "Nieren geprüft werden kann. \n \n  " \
                   "Sollten Berechnungen unrichtig sein, geht davon aus, dass der \n" \
                   "Fehler eher bei dem Programm, als bei der Lohnbuchhaltung \n" \
                   "liegt. Das soll sich natürlich bald ändern. \n \n" \
                   "Daher bitte ich Euch, mir alle sachdienlichen Hinweise an \n" \
                   "simonbeyer79@gmail.com zu schicken.\n \n" \
                   "Selbstverständlich ist noch sehr viel zu tun, \n " \
                   "beispielsweise fehlen noch folgende Dinge: \n \n" \
                   "- die Berechnung des Wegegeldes für die \n kurzfristige Vermittlung\n" \
                   "- die Zahlungen für die Corona-Tests \n" \
                   "- die Zusammenfassung mehrerer kurzer Schichten oder ATs bei\n" \
                   "der Berechnung des Verpflegungsmehraufwands \n" \
                   "- Automatische Erstellung von BSD-Zetteln, Urlaubsanträgen usw.\n" \
                   "- auf lange Sicht soll das Programm nicht ausschließlich\n lokal bleiben, so dass \n" \
                   "   weitere features geplant werden können. \n" \
                   "- eine Handy-App als 'AT-Modus'\n    (schnelles Schichten Eintragen beim gleichen ASN)\n" \
                   "- vielleicht noch eine ASN.Oberfläche, Dienstplanung \n" \
                   "und was man sich sonst noch vorstellen kann"


        hallo = tk.Label(self, text=infotext, justify="left")
        hallo.grid(row=0, column=0)
