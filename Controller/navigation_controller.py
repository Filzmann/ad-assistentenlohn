from datetime import datetime

from View.navigation_view import NavigationView


class NavigationController:
    def __init__(self, parent_controller, session, parent_view, controlled_areas: {}):
        self.view = NavigationView(parent_view=parent_view)
        self.controlled_areas = controlled_areas
        # self.offset = 0
        self.arbeitsdate = datetime.now()
        self.view.vormonat.config(command=lambda: self.monat_change(-1))
        self.view.naechster_monat.config(command=lambda: self.monat_change(1))

    def monat_change(self, step=None, datum: datetime = None):
        if datum:
            self.arbeitsdate = datetime(year=datum.year, month=datum.month, day=1)
        else:
            # self.offset += step
            self.arbeitsdate = self.berechne_arbeitsdate(step)
            self.arbeitsdate = datetime(self.arbeitsdate.year,
                                        self.arbeitsdate.month,
                                        1)
        self.view.aktueller_monat.config(text=self.arbeitsdate.strftime("%B %Y"))

        self.controlled_areas['tabelle'].change_arbeitsdatum(datum=self.arbeitsdate)
        self.controlled_areas['summen'].change_arbeitsdatum(datum=self.arbeitsdate)

    def berechne_arbeitsdate(self, step=0):
        # lieber datum der letzten eingetragenen schicht
        dt = self.arbeitsdate
        # dt = self.assistent.letzte_eingetragene_schicht.beginn
        aktuelles_datum = datetime(year=dt.year, month=dt.month, day=1)
        jahrmonat = divmod(aktuelles_datum.month + step, 12)
        jahroffset = jahrmonat[0]
        monat = jahrmonat[1]
        if monat == 0:
            monat = 12
            jahroffset -= 1
        return datetime(year=aktuelles_datum.year + jahroffset, month=monat, day=1)
