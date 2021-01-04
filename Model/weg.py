from sqlalchemy import create_engine, ForeignKey, Column, Integer
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class Weg(Base):
    __tablename__ = 'weg'

    id = Column(Integer, primary_key=True)
    adresse1 = Column(Integer, ForeignKey('adresse.id'))
    adresse2 = Column(Integer, ForeignKey('adresse.id'))


    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
