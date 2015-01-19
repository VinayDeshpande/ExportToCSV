from pyramid.view import view_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import User
from sqlalchemy.orm import sessionmaker
import csv
from pyramid.response import Response
import os
import time
from models import Points
from shapely import wkt
from shapely.geometry import Point
import geoalchemy2.functions as geofunc
from sqlalchemy.sql import label
import json
from shapely.wkt import dumps, loads
from shapely.geometry import mapping, shape

engine = create_engine('postgresql://vinay:aditi@localhost:5432/eventsapp')

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()




@view_config(route_name='disp', renderer='templates/homepage.pt')
def new_view(request):

    return {'hello': " "}


@view_config(route_name='home', renderer='templates/homepage.pt')
def export_view(request):
    st = time.time()
    download_path = os.getcwd() + '/'+'test.csv'
    list1 = session.query(User).all()
    f = open('test.csv', 'wb')
    for row in list1:
        l = [row.id, row.Name, row.Email_id, row.Address]

        wr = csv.writer(f, dialect='excel')
        wr.writerow(l)
    f.close()

    response = Response(content_type='application/force-download', content_disposition='attachment; filename='+ 'test.csv')
    response.app_iter = open(download_path, 'rb')
    end = time.time()
    el = end-st
    print "EXPORT",
    print el,
    print "SECONDS"
    return response


@view_config(route_name='importroute', renderer='templates/homepage.pt')
def import_view(request):
    start = time.time()
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
                end = time.time()
                elap = end-start
                print "IMPORT",
                print elap,
                print "SECONDS"
        else:
                return {"hello": "ENTER THE NAME OF THE FILE!!!!!!!"}
    return {"hello": "Inserted Into the database!!!"}


@view_config(route_name='latlong', renderer='templates/Secondpage.pt')
def latlong_view(request):

    return {'hello': " CALCULATE THE DISTANCE BETWEEN TWO POINTS!! "}


@view_config(route_name='display', renderer='templates/Secondpage.pt')
def diplay_view(request):

    po = label('po', geofunc.ST_AsGeoJSON(Points.points))
    item = session.query(Points, po)
    item = item.all()
    # print "#######", type(item)
    points=None
    for i in item:
        # print dir(i)
        # print i.__getattribute__

        # l=[]
        # l=i.points

        # print st
        points = json.loads(i.po).get('coordinates')
        points = Point(points[0], points[1])
        print points

    return {"hello": points}