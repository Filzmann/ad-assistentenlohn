from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Model.base import Base


class Adresse(Base):
    __tablename__ = 'adressen'

    id = Column(Integer, primary_key=True)
    bezeichner = Column(String(30))
    strasse = Column(String(30))
    hausnummer = Column(String(8))
    plz = Column(String(5))
    stadt = Column(String(30))

    # one to many AS
    assistent_id = Column(Integer, ForeignKey('assistenten.id'))
    assistent = relationship("Assistent", back_populates='adressbuch')

    # one to many ASN
    assistenznehmer_id = Column(Integer, ForeignKey('assistenznehmer.id'))
    assistenznehmer = relationship("ASN", back_populates='adressbuch')

    wege = relationship("Weg", primaryjoin="or_(Adresse.id==Weg.adresse1_id, Adresse.id==Weg.adresse2_id)")

    def __repr__(self):
        return f"Address(id={self.id!r}, " \
               f"strasse={self.strasse!r}, " \
               f"hausnummer={self.hausnummer!r}, " \
               f"plz={self.plz!r})"
