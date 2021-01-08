from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Model.base import Base


class Assistent(Base):
    __tablename__ = 'assistenten'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    einstellungsdatum = Column(DateTime)
    home_id = Column(Integer, ForeignKey('adressen.id'))
    home = relationship("Adresse",
                        back_populates="assistent",
                        primaryjoin="Assistent.home_id==Adresse.id")

    schichten = relationship("Schicht")
    urlaub = relationship("Urlaub")

    def __repr__(self):
        return f"Assistent({self.name!r}, {self.vorname!r})"
