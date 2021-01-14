from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from Model.base import Base


class AssociationAsAsn(Base):
    __tablename__ = 'association_as_asn'
    as_id = Column(Integer, ForeignKey('assistenten.id'), primary_key=True)
    asn_id = Column(Integer, ForeignKey('assistenznehmer.id'), primary_key=True)
    fest_vertretung = Column(String(50))
    assistenten = relationship("Assistent", back_populates="asn")
    asn = relationship("ASN", back_populates="assistenten")
