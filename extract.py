# UrbanETL Extract Functions
# 8/15/2016

# This file is a wrapper for petl extract functions. There is very little
# structure to this code; it essentially determines from the input string what
# kind of extract strategy to execute, unless specified by the user.

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

# When you add a supported format, please add it to the SUPPORTED global for
# reference purposes, in the order added.

SUPPORTED = ['csv', 'pandas']

class UrbanExtract():

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
            try:
                self.data = petl.io.fromcsv(self.datasource)
                print "    Data extracted successfully."
            except Exception as e:
                print "    ERROR: Cannot read csv file. {}".format(e)

        if self.datatype == 'pandas':
            try:
                self.data = petl.io.fromdataframe(self.datasource, include_index=False))
            except Exception as e:
                print "    ERROR: Cannot read pandas dataframe. {}".format(e)

        else:
            print "    This datasource type is not yet supported."
            print "    Urban ETL currently supports the following data formats:\n"
            for x in SUPPORTED:
                print x

    def load(self, filetype, destination, **args):
        '''
        A nest of if statements by type to output to a destination.

        Can take additional arguments depending on type.
        '''
        if filetype == 'csv':
            # can pass any arguments accepted by csv
            petl.io.csv.tocsv(self.data, **args)
        if filetype == 'pandas':
            # Additional arguments:
            #   index=None, exclude=None, columns=None, coerce_float=False, nrows=None
            petl.io.pandas.todataframe(self.data, **args)
