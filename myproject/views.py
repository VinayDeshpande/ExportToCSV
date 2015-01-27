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
from shapely.geometry import Point, LineString
import geoalchemy2.functions as geofunc
from sqlalchemy.sql import label
import json
from shapely.wkt import dumps, loads
from shapely.geometry import mapping, shape
import itertools
import math
from models import ZoneGeoms
from collections import OrderedDict

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
        print l
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

    po = label('po', geofunc.ST_AsGeoJSON(Points.coords))
    item = session.query(Points, po)
    item = item.all()
    points = []
    for i in item:
        coords = json.loads(i.po).get('coordinates')
        position = (coords[0], coords[1]) #tuple (x, y)
        points.append(position) #list [(x, y), (x, y)]
    distances = {}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            pt1 = points[i]
            pt2 = points[j]
            pts = (pt1, pt2)
            a = abs((pt2[0] - pt1[0]) ** 2)
            b = abs((pt2[1] - pt1[1]) ** 2)
            dist = math.sqrt(a + b)

            distances[pts] = dist


    sorted_dict =sorted(distances.items(), key=lambda x: x[1])
    print sorted_dict[0:5]
    return {"hello": " "}


@view_config(route_name='kml', renderer='templates/Secondpage.pt')
def kml_view(request):

    outfile = file("file1.kml", 'w')
    download_path = os.getcwd() + '/'+'file1.kml'
    data = session.query(ZoneGeoms).all()

    l1 = []
    for row in data:
        l = {
            'row_id': row.id,
            'row_name': row.name,
            'row_geom': row.geom,
            'row_description': row.description
        }
        l1.append(l)

    for x in l1:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        outfile.write('<placemark>\n')
        outfile.write('  <row>\n')
        outfile.write('    <id>%s</id>\n' % x['row_id'])
        outfile.write('    <name>%s</name>\n' % x['row_name'])
        outfile.write('    <geom>%s</geom>\n' % x['row_geom'])
        outfile.write('    <description>%s</description>\n' % x['row_description'])
        outfile.write('  </row>\n')
        outfile.write('</placemark>\n')


    response = Response(content_type='application/force-download', content_disposition='attachment; filename='+ 'file1.kml')
    response.app_iter = open(download_path, 'rb')
    outfile.close()

    return response




