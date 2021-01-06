from sqlalchemy import create_engine, ForeignKey, Column, Integer, Float
from sqlalchemy.orm import declarative_base, relationship

from Model.base import Base


class Weg(Base):
    __tablename__ = 'wege'

    id = Column(Integer, primary_key=True)
    entfernung = Column(Float)
    dauer_in_minuten = Column(Integer)
    adresse1_id = Column(Integer, ForeignKey('adressen.id'))
    adresse2_id = Column(Integer, ForeignKey('adressen.id'))

    def __repr__(self):
        return f"Address(id={self.id!r}, " \
               f"Adresse1={self.adresse1_id!r}, " \
               f"Adresse2={self.adresse2_id!r})"
