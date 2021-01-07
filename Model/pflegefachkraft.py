from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class PFK(Base):
    __tablename__ = 'pflegefachkraefte'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    assistenznehmer = relationship("ASN", back_populates="pflegefachkraefte")