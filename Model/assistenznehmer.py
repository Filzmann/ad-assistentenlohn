from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base
from Model.association_as_asn import AssociationAsAsn


class ASN(Base):
    __tablename__ = 'assistenznehmer'

    id = Column(Integer, primary_key=True)
    kuerzel = Column(String, nullable=False)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    # one to one
    home_id = Column(Integer, ForeignKey('adressen.id'))
    home = relationship("Adresse",
                        back_populates="assistenznehmer",
                        primaryjoin="ASN.home_id==Adresse.id")

    assistenten = relationship(
        "AssociationAsAsn", back_populates="asn")

    # one to many
    # adressbuch = relationship("Adresse")

    einsatzbuero = Column(String(30))
    schicht_templates = relationship("SchichtTemplates")
    schichten = relationship("Schicht")
    eb_id = Column(Integer, ForeignKey('einsatzbegleitungen.id'))
    einsatzbegleitung = relationship("EB", back_populates="assistenznehmer")
    pfk_id = Column(Integer, ForeignKey('pflegefachkraefte.id'))
    pflegefachkraft = relationship("PFK", back_populates="assistenznehmer")

    def __repr__(self):
        return f"(id={self.id!r}, Kürzel={self.kuerzel!r}, Name={self.name!r}, Vorname={self.vorname!r})"
