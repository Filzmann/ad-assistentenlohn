from datetime import datetime

from View.navigation_view import NavigationView


class NavigationController:
    def __init__(self, parent_controller, session, parent_view, controlled_areas: {}):
        self.session = session

        monatsarray = dict((monat, datetime(year=1, month=monat, day=1).strftime('%b')) for monat in range(1, 13))
        jahrarray = dict((jahr, jahr) for jahr in range(datetime.now().year, 1980, -1))

        # auf list umstellen und dropdown ensprechend modifizieren
        # jahrarray = [x for x in range(datetime.now().year, 1980, -1)]

        self.view = NavigationView(parent_view=parent_view,
                                   monatsarray=monatsarray,
                                   jahrarray=jahrarray)

        self.view.monats_dropdown.set(datetime.now().month)
        self.view.jahr_dropdown.set(datetime.now().year)
        self.controlled_areas = controlled_areas
        # self.offset = 0
        self.arbeitsdate = datetime.now()

        self.view.vormonat.config(command=lambda: self.monat_change(step=-1, session=self.session))
        self.view.naechster_monat.config(command=lambda: self.monat_change(step=1, session=self.session))
        self.view.changebutton.config(command=lambda: self.changebutton())

    def monat_change(self, session, step=None, datum: datetime = None):
        if datum:
            self.arbeitsdate = datetime(year=datum.year, month=datum.month, day=1)
        else:
            # self.offset += step
            self.arbeitsdate = self.berechne_arbeitsdate(step)
            self.arbeitsdate = datetime(self.arbeitsdate.year,
                                        self.arbeitsdate.month,
                                        1)
        self.view.aktueller_monat.config(text=self.arbeitsdate.strftime("%B %Y"))

        self.controlled_areas['tabelle'].change_arbeitsdatum(datum=self.arbeitsdate, session=session)
        self.controlled_areas['summen'].change_arbeitsdatum(datum=self.arbeitsdate, session=session)

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

    def changebutton(self):
        jahr = self.view.jahr_dropdown.get()
        monat = self.view.monats_dropdown.get()
        datum = datetime(year=jahr, month=monat, day=1)
        self.monat_change(session=self.session, step=None, datum=datum)
