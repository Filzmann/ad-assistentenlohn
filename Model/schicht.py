from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class Schicht(Base):
    __tablename__ = 'schichten'

    id = Column(Integer, primary_key=True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    asn_id = Column(Integer, ForeignKey('assistenznehmer.id'))
    asn = relationship("ASN", back_populates="schichten")
    assistent_id = Column(Integer, ForeignKey('assistenten.id'))
    assistent = relationship("Assistent", back_populates="schichten")
    ist_kurzfristig = Column(Boolean)
    ist_ausfallgeld = Column(Boolean)
    ist_assistententreffen = Column(Boolean)
    ist_pcg = Column(Boolean)
    ist_schulung = Column(Boolean)
    beginn_andere_adresse = Column(Integer, ForeignKey('adressen.id'))
    ende_andere_adresse = Column(Integer, ForeignKey('adressen.id'))

    def __repr__(self):
        return f"Schicht( Beginn: {self.beginn!r}, Ende: {self.ende!r}, ASN: {self.asn!r})"
