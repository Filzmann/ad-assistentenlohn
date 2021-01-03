from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    assistent_id = Column(Integer, ForeignKey('assistent.id'))
    assistenznehmer_id = Column(Integer, ForeignKey('assistenznehmer.id'))



    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
