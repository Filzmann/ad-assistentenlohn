from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from Model.base import Base


class SchichtTemplate(Base):
    __tablename__ = 'schicht_templates'

    id = Column(Integer, primary_key=True)

    # relationships
    asn_id = Column(Integer, ForeignKey('assistenznehmer.id'))
    asn = relationship("ASN", back_populates="schicht_templates")

    # extra data
    beginn = Column(DateTime)
    ende = Column(DateTime)
    bezeichner = Column(String(30))

    def __repr__(self):
        return f"Template({self.bezeichner!r}, {self.beginn!r} - {self.ende!r})"
