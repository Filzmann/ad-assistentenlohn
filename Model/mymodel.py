from Models import Base
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value
