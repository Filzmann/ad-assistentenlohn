from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from Model.adresse import Adresse
from Model.base import Base


class ASN(Base):
    __tablename__ = 'assistenznehmer'

    id = Column(Integer, primary_key=True)
    kuerzel = Column(String, nullable=False)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    assistenten = relationship(
        "AssociationAsAsn", back_populates="asn")

    # hier stehen alle Adressen des ASN, auch die eigene. Diese erhält den bezeichner __home__
    adressbuch = relationship("Adresse", back_populates="assistenznehmer")

    einsatzbuero = Column(String(30))
    schicht_templates = relationship("SchichtTemplate",
                                     back_populates="asn",
                                     cascade="all, delete, delete-orphan")
    schichten = relationship("Schicht", back_populates="asn")
    feste_schichten = relationship("FesteSchicht",
                                   back_populates="asn",
                                   cascade="all, delete, delete-orphan")
    eb_id = Column(Integer, ForeignKey('einsatzbegleitungen.id'))
    einsatzbegleitung = relationship("EB", back_populates="assistenznehmer")
    pfk_id = Column(Integer, ForeignKey('pflegefachkraefte.id'))
    pflegefachkraft = relationship("PFK", back_populates="assistenznehmer")

    def __repr__(self):
        return f"ASN(id={self.id!r}, Kürzel={self.kuerzel!r}, Name={self.name!r}, Vorname={self.vorname!r})"
