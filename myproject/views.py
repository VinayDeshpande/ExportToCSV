from pyramid.view import view_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import User
from sqlalchemy.orm import sessionmaker
import csv
from pyramid.response import Response
import os

engine = create_engine('postgresql://vinay:aditi@localhost:5432/eventsapp')

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()




@view_config(route_name='disp', renderer='templates/homepage.pt')
def new_view(request):

    return {'hello': ""}


@view_config(route_name='home', renderer='templates/homepage.pt')
def export_view(request):
    download_path = os.getcwd() + '/'+'test3.csv'
    list1 = session.query(User).all()
    f = open('test3.csv', 'wb')
    for row in list1:
        l = [row.id, row.Name, row.Email_id, row.Address]

        wr = csv.writer(f, dialect='excel')
        wr.writerow(l)
    f.close()

    response = Response(content_type='application/force-download', content_disposition='attachment; filename='+ 'test3.csv')
    response.app_iter = open(download_path, 'rb')
    return response

@view_config(route_name='importroute', renderer='templates/homepage.pt')
def import_view(request):
    if request.method == 'POST':
        filename = request.POST.get('filename')
        if filename:
            try:
                reader = csv.reader(open(filename, 'rb'))
                print reader, type(reader)
            except IOError:
                return {"hello": "NO SUCH FILE OR DIRECTORY!!!!"}
            else:
                for row in reader:
                    if len(row) >= 3:
                        e = User(Name=row[0], Email_id=row[1], Address=row[2])
                        session.add(e)
                    else:
                        return {"hello": "Choose the correct file"}
                session.commit()
        else:
                return {"hello": "ENTER THE NAME OF THE FILE!!!!!!!"}
    return {"hello": "Inserted Into the database!!!"}