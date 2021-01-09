from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


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

    # one to many
    # adressbuch = relationship("Adresse")


    schicht_templates = relationship("SchichtTemplates")
    schichten = relationship("Schicht")
    eb_id = Column(Integer, ForeignKey('einsatzbegleitungen.id'))
    einsatzbegleitungen = relationship("EB", back_populates="assistenznehmer")
    pfk_id = Column(Integer, ForeignKey('pflegefachkraefte.id'))
    pflegefachkraefte = relationship("PFK", back_populates="assistenznehmer")

    def __repr__(self):
        return f"Assistent(id={self.id!r}, Name={self.name!r}, Vorname={self.vorname!r})"
