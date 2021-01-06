from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Model.base import Base


class Assistent(Base):
    __tablename__ = 'assistenten'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    einstellungsdatum = Column(DateTime)
    home = relationship("Adresse", back_populates="assistent")
    schichten = relationship("Schicht")
    urlaub = relationship("Urlaub")

    def __repr__(self):
        return f"Assistent(id={self.id!r}, Name={self.name!r}, Vorname={self.vorname!r})"
