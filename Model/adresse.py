from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from Model.base import Base


class Adresse(Base):
    __tablename__ = 'adressen'

    id = Column(Integer, primary_key=True)
    strasse = Column(String(30))
    hausnummer = Column(String(8))
    plz = Column(String(5))
    stadt = Column(String(30))
    assistent_id = Column(Integer, ForeignKey('assistenten.id'))
    assistent = relationship("Assistent", back_populates="home")
    assistenznehmer_id = Column(Integer, ForeignKey('assistenznehmer.id'))
    assistenznehmer = relationship("ASN", back_populates="home")
    wege = relationship("Weg", primaryjoin="or_(Adresse.id==Weg.adresse1_id, Adresse.id==Weg.adresse2_id)")


    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
