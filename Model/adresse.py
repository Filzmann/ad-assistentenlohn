from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class Adresse(Base):
    __tablename__ = 'adressen'

    id = Column(Integer, primary_key=True)
    strasse = Column(String(30))
    hausnummer = Column(String(8))
    plz = Column(String(5))
    stadt = Column(String(30))
    assistent_id = Column(Integer, ForeignKey('assistent.id'))
    assistenznehmer_id = Column(Integer, ForeignKey('assistenznehmer.id'))
    wege = relationship("Weg", back_populates="adressen")


    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
