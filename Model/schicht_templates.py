from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class SchichtTemplates(Base):
    __tablename__ = 'schicht_templates'

    id = Column(Integer, primary_key=True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    bezeichner = Column(String(30))
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))

