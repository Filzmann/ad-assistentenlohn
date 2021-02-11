from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class Lohn(Base):
    __tablename__ = 'loehne'

    id = Column(Integer, primary_key=True)
    erfahrungsstufe = Column(Integer)
    gueltig_ab = Column(DateTime)
    eingruppierung = Column(Integer)
    grundlohn = Column(Float)
    nacht_zuschlag = Column(Float)
    samstag_zuschlag = Column(Float)
    sonntag_zuschlag = Column(Float)
    feiertag_zuschlag = Column(Float)
    wechselschicht_zuschlag = Column(Float)
    orga_zuschlag = Column(Float)
    ueberstunden_zuschlag = Column(Float)
    hl_abend_zuschlag = Column(Float)
    silvester_zuschlag = Column(Float)
