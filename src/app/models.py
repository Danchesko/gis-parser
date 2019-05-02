import os

from sqlalchemy import Column, String, Integer, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DoubleGis(Base):
    __tablename__='doublegis'

    url = Column(String, primary_key=True, nullable=False)
    title = Column(String)
    numbers = Column(ARRAY(String))
    address = Column(String)
    instagram = Column(String)
    email = Column(String)
    website = Column(String)
    html = Column(String)
    





