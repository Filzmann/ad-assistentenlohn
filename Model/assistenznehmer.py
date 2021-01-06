from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ASN(Base):
    __tablename__ = 'assistenten'

    id = Column(Integer, primary_key=True)
    kuerzel = Column(String, nullable=False)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    home = relationship("Address", back_populates="user")
    adressen = relationship("Address")
    schicht_templates = relationship("SchichtTemplates")
    schichten = relationship("Schicht")
    eb_id = Column(Integer, ForeignKey('einsatzbegleitung.id'))
    einsatzbegleitung = relationship("EB", back_populates="children")
    pfk_id = Column(Integer, ForeignKey('pflegefachkraft.id'))
    pflegefachkraft = relationship("PFK", back_populates="children")

    def __repr__(self):
        return f"Assistent(id={self.id!r}, Name={self.name!r}, Vorname={self.vorname!r})"
