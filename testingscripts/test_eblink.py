# Testing code for eblink insertion

import urbanetl as ub

def run():
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    rv = data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('lname_c1', 'lname_c1', 'lname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 's', 'c', 'c', 'c'], iterations = 300)
    return rv
