# UrbanETL Extract Functions
# 8/15/2016

# This file is a wrapper for petl extract and load functions. There is very
# little structure to this code; it essentially determines from the input string
# what kind of extract strategy to execute, unless specified by the user.

# petl documentation: https://petl.readthedocs.io/en/latest/index.html
# For any datasource, regardless of type, self.data is an iterable data type
# that returns one tuple per row, where the first row are headers.

# To add additional functionality, simply extend the if statements to include
# a function that deals with the file type or database necessary. Check against
# petl's existing code base to make sure that there isn't an existing
# representation -- there likely is, it's pretty extensive.

# This code also includes basic utility functions.

import petl
import csv
# import transform
# import transform
# transform.path.append('../transform')


# When you add a supported format, please add it to the SUPPORTED global for
# reference purposes, in the order added.

SUPPORTED = ['csv', 'pandas'] # '.xlsx', '.xlrd', '.xlwt', '.xls', '.dta', '.csv'
#'.json','.html']

class Extract(object):

    '''
    Return an Extract object whose data is *data read from the *datasource
    with *datatype
    '''

    def __init__(self, datasource, datatype=None, args = ()):
        self.datasource = datasource
        self.datatype = datatype
        self.data = None
        self.read()

    def read(self):
        '''
        A nest of booleans to determine which extract function to call.
        See the SUPPORTED global for currently supported file types.
        '''
        if self.datatype == 'csv' or '.csv' in self.datasource:
            ### CSV ###
            try:
                self.data = petl.io.fromcsv(self.datasource)
                print "----> Data extracted successfully."
                return
            except Exception as e:
                print "----> ERROR: Cannot read csv file. {}".format(e)
        if self.datatype == 'pandas':
            ### PANDAS ###
            try:
                self.data = petl.io.fromdataframe(self.datasource, include_index=False)
                print "----> Data extracted successfully."
                return
            except Exception as e:
                print "----> ERROR: Cannot read pandas dataframe. {}".format(e)
        else:
            ### ERROR MESSAGE ###
            print "----> This datasource type is not yet supported or cannot be determined."
            print "----> If datasource type is supported, please specify using datatype."
            print "----> Urban ETL currently supports the following data formats:\n"
            for x in SUPPORTED:
                print "        {}".format(x)

    def load(self, desttype, destination=None, **kargs):
        '''
        A nest of booleans to load table into destination.

        Can take additional arguments depending on type.
        '''
        ### CSV ###
        if desttype == 'csv':
            # can pass any arguments accepted by csv
            petl.io.csv.tocsv(self.data, destination, **kargs)
            print "----> Data written to {}.".format(destination)

        ### PANDAS ###
        if desttype == 'pandas':
            # Additional arguments:
            #   index=None, exclude=None, columns=None, coerce_float=False, nrows=None
            return petl.io.pandas.todataframe(self.data, **kargs)

        ### ERROR MESSAGE ###
        else:
            print "----> This destination type is not yet supported."
            print "----> Urban ETL currently supports the following data formats:\n"
            for x in SUPPORTED:
                print "        {}".format(x)
