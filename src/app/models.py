import os

from sqlalchemy import Column, String, Integer, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DoubleGis(Base):
    __tablename__='doublegis'
    id = Column(Integer, primary_key = True)
    title = Column(String)
    numbers = Column(ARRAY(String))
    address = Column(String)
    url = Column(String)
    email = Column(String)
    website = Column(String)

class DoubleGisBody(Base):
    __tablename__='doublegis-html'
    id = Column(Integer, primary_key=True)
    parent_id=Column(Integer, ForeignKey('doublegis.id'))
    html = Column(String)





