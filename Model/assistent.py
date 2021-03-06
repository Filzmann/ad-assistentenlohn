from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from Model.base import Base
from Model.association_as_asn import AssociationAsAsn


class Assistent(Base):
    __tablename__ = 'assistenten'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    einstellungsdatum = Column(DateTime)
    adressbuch = relationship("Adresse", back_populates="assistent")
    asn = relationship("AssociationAsAsn", back_populates="assistenten")
    feste_schichten = relationship("FesteSchicht",
                                   back_populates="assistent",
                                   cascade="all, delete, delete-orphan")
    schichten = relationship("Schicht", back_populates="assistent")
    urlaub = relationship("Urlaub")

    def __repr__(self):
        return f"Assistent({self.name!r}, {self.vorname!r})"
