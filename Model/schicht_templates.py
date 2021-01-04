from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class SchichtTemplates(Base):
    __tablename__ = 'adressen'

    id = Column(Integer, primary_key=True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    bezeichner = Column(String(30))
    asn = Column(Integer, ForeignKey('assistenznehmer.id'))

