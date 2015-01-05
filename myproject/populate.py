from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

Base = declarative_base()

engine = create_engine('postgresql://vinay:aditi@localhost:5432/eventsapp')

Session = sessionmaker(bind=engine)

session = Session()

# e = User()
# e.id = '20'
# e.Name = 'DESHPANDE'
# e.Address = 'AGB Layout'
# e.Email_id = 'vinayd@gmail.com'
# session.add(e)
# session.commit()
