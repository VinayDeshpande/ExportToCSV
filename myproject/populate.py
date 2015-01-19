from settings import *


session.add_all([
    Points(name='MSDHONI', assets='BMW', points='POINT(1 1)'),
    Points(name='SACHIN', assets='AUDI', points='POINT(3 2)'),
    Points(name='VIRAT', assets='MARUTI', points='POINT(2 3)'),
    Points(name='ROHIT', assets='JAQUAR', points='POINT(4 1)'),
    Points(name='BHUVI', assets='VOLVO', points='POINT(5 2)'),
    Points(name='SURESH', assets='FIAT', points='POINT(1 3)'),
    Points(name='ASHWIN', assets='SUZUKI', points='POINT(2 1)'),
    Points(name='RAHANE', assets='TATA', points='POINT(4 2)'),
    Points(name='DHAWAN', assets='VOLKSWAGON', points='POINT(2 1)'),


])

session.commit()



