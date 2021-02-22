from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class Brutto(Base):
    __tablename__ = 'bruttolohn'

    id = Column(Integer, primary_key=True)
    monat = Column(DateTime)
    bruttolohn = Column(Float)
    stunden_gesamt = Column(Float)
    as_id = Column(Integer)

    def __repr__(self):
        return f"{self.id} {self.monat} {self.bruttolohn} {self.stunden_gesamt}"
