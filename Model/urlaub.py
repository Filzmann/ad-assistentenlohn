from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class Urlaub(Base):
    __tablename__ = 'schichten'
    assistent = Column(Integer, ForeignKey('assistent.id'))
    beginn = beginn
    ende = ende
    status = status
