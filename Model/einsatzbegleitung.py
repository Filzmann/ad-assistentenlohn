from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class EB(Base):
    __tablename__ = 'einsatzbegleitungen'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    assistenznehmer = relationship("ASN", back_populates="einsatzbegleitungen")

    def __repr__(self):
        return f"{self.name!r}, {self.vorname!r})"
