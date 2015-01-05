from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


engine = create_engine('postgresql://vinay:aditi@localhost:5432/eventsapp')

Base = declarative_base()


class User(Base):
    __tablename__= 'user'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Address = Column(String)
    Email_id = Column(String)


Base.metadata.create_all(engine)