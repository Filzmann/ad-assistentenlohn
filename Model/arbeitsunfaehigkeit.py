from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Model.base import Base


class AU(Base):
    __tablename__ = 'arbeitsunfaehigkeit'

    id = Column(Integer, primary_key=True)
    assistent = Column(Integer, ForeignKey('assistenten.id'))
    beginn = Column(DateTime)
    ende = Column(DateTime)

