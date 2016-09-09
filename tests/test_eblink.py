# Testing code for eblink insertion

import urbanetl as ub

def run():
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    rv = data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('lname_c1', 'lname_c1', 'lname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 's', 'c', 'c', 'c'], iterations = 500)
    return rv

def test1(): # one fewer column, fewer iterations
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    rv = data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 'c', 'c', 'c'], iterations = 300)
    return rv

def test2(): # mislabeled types
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    rv = data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('lname_c1', 'lname_c1', 'lname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 'c', 'c', 'c', 'c'], iterations = 300)
    return rv

def test3(): # Drop a dataset
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    rv = data1.link(data=[data2], links=[('fname_c1', 'fname_c1'),
    ('lname_c1', 'lname_c1'), ('by', 'by'), ('bm', 'bm'), ('bd', 'bd')],
    uids=['UID', 'UID'], types=['s', 's', 'c', 'c', 'c'], iterations = 300)
    return rv

def test4(): # Interactive build
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    return data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('lname_c1', 'lname_c1', 'lname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 's', 'c', 'c', 'c'], iterations = 500, out = 'inter')

def test5(): # Non-interactive build
    data1 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_1.csv')
    data2 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_2.csv')
    data3 = ub.UrbanETL('linkagepackages/graphical-record-linkage/python-encapsulation/test_data/RLData500_3.csv')
    return data1.link(data=[data2, data3], links=[('fname_c1', 'fname_c1',
    'fname_c1'), ('lname_c1', 'lname_c1', 'lname_c1'), ('by', 'by', 'by'),
    ('bm', 'bm', 'bm'), ('bd', 'bd', 'bd')], uids=['UID', 'UID', 'UID'],
    types=['s', 's', 'c', 'c', 'c'], iterations = 500, out = 'linked')
