from sqlalchemy import ForeignKey, Column, Integer, String
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
    # one to one
    assistent = relationship("Assistent",
                             back_populates="home",
                             uselist=False,
                             primaryjoin="Adresse.id==Assistent.home_id"
                             )
    # one to one
    assistenznehmer = relationship("ASN",
                                   back_populates="home",
                                   uselist=False,
                                   primaryjoin="Adresse.id==ASN.home_id")
    # many to one
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))

    wege = relationship("Weg", primaryjoin="or_(Adresse.id==Weg.adresse1_id, Adresse.id==Weg.adresse2_id)")

    def __repr__(self):
        return f"Address(id={self.id!r}, " \
               f"strasse={self.strasse!r}, " \
               f"hausnummer={self.hausnummer!r}, " \
               f"plz={self.plz!r})"
