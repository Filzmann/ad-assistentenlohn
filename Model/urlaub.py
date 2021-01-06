from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Model.base import Base


class Urlaub(Base):
    __tablename__ = 'urlaub'

    id = Column(Integer, primary_key=True)
    assistent = Column(Integer, ForeignKey('assistenten.id'))
    beginn = Column(DateTime)
    ende = Column(DateTime)
    status = Column(String(10))
