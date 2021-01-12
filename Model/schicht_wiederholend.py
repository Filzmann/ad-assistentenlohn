from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class SchichtRegelmaessig(Base):
    __tablename__ = 'schichten_regelmaessig'

    id = Column(Integer, primary_key=True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))
    assistent = Column(Integer, ForeignKey('assistenten.id'))
    wochentag = Column(Integer)
