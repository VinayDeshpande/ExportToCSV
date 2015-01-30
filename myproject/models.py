from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

engine = create_engine('postgresql://vinay:aditi@localhost:5432/eventsapp')

Base = declarative_base()


class User(Base):
    __tablename__= 'user'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Address = Column(String)
    Email_id = Column(String)

# class Zone(Base):
#     __tablename__ = 'zone'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     points = Column(Geometry('POINT'))
#     assets = Column(String)
#
class Points(Base):
    __tablename__ = 'points '

    id = Column(Integer, primary_key=True)
    name = Column(String)
    coords = Column(Geometry('POINT'))
    assets = Column(String)


class ZoneGeoms(Base):
    __tablename__ = 'zonegeoms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POLYGON'))
    description = Column(String)

class ZoneGeomPoly(Base):
    __tablename__ = "zonegeompoly"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    outerboundary = Column(Geometry('POLYGON'))
    innerboundary = Column(Geometry('POLYGON'))


Base.metadata.create_all(engine)