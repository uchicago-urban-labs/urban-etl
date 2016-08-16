# UrbanETL Extract Functions
# 8/15/2016

# This file is a wrapper for petl extract functions. There is very little
# structure to this code; it essentially determints from the input what kind of
# extract strategy to execute, unless specified by the user.

# petl documentation: https://petl.readthedocs.io/en/latest/index.html

# To add additional functionality, simply extend the if statements to include
# a function that deals with the file type or database necessary.

# This code also includes basic utility functions.

import petl

class UrbanExtract:

    def __init__(self, datasource, datatype=None):
        self.datasource = datasource
        self.datatype = datatype
        self.data = None
        self.call_read()

    def call_read(self):
        '''
        A nest of if statements to determine which extract function to call.
        '''
