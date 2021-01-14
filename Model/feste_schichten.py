from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class FesteSchicht(Base):
    __tablename__ = 'feste_schichten'

    id = Column(Integer, primary_key=True)
    assistent = Column(Integer, ForeignKey('assistenten.id'))
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))

    # extra Data
    wochentag = Column(String(10))
    beginn = Column(DateTime)
    ende = Column(DateTime)
