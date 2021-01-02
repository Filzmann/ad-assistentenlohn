from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base = declarative_base()


class Weg(Base):
    __tablename__ = 'weg'

    id = Column(Integer, primary_key=True)
    address1 = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
