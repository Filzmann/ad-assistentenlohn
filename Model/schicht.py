from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class Schicht(Base):
    __tablename__ = 'schichten'

    id = Column(Integer, primary_key=True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))
    assistent = Column(Integer, ForeignKey('assistenten.id'))
    # teilschichten = relationship("Schicht", back_populates="schicht")
    # original_schicht_id = Column(Integer, ForeignKey('schicht.id'))
    # original_schicht = relationship("Schicht", back_populates='schicht')
    # TODO delete-orphan anschauen um vermüllen der Tabelle zu verhindern
    ist_kurzfristig = Column(Boolean)
    ist_ausfallgeld = Column(Boolean)
    ist_assistententreffen = Column(Boolean)
    ist_pcg = Column(Boolean)
    ist_schulung = Column(Boolean)
    beginn_andere_adresse = Column(Integer, ForeignKey('adressen.id'))
    ende_andere_adresse = Column(Integer, ForeignKey('adressen.id'))

    # stundenzahl = self.berechne_stundenzahl()
    # stundenlohn = assistent.lohntabelle.get_grundlohn(self.beginn)
    # schichtlohn = self.stundenzahl * self.stundenlohn
    # wechselschichtzulage = assistent.lohntabelle.get_zuschlag('Wechselschicht', beginn)
    # wechselschichtzulage_schicht = self.wechselschichtzulage * self.stundenzahl
    # orgazulage = assistent.lohntabelle.get_zuschlag('Orga', beginn)
    # orgazulage_schicht = self.orgazulage * self.stundenzahl
    # nachtstunden = self.berechne_anzahl_nachtstunden()
    # nachtzuschlag = assistent.lohntabelle.get_zuschlag('Nacht', beginn)
    # nachtzuschlag_schicht = self.nachtstunden * self.nachtzuschlag
    # zuschlaege = self.berechne_sa_so_weisil_feiertagszuschlaege()
