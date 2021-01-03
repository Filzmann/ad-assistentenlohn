from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class ASN(Base):
    __tablename__ = 'assistenten'

    id = Column(Integer, primary_key=True)
    kuerzel = Column(String, nullable=False)
    name = Column(String(30))
    vorname = Column(String(30))
    email = Column(String(30))
    home = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"Assistent(id={self.id!r}, Name={self.name!r}, Vorname={self.vorname!r})"
