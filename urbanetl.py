# UrbanETL
# 8/15/2016

# This file is a wrapper for petl unctions. There is very
# little structure to this code; it essentially determines from the input string
# what kind of extract strategy to execute, unless specified by the user.

# petl documentation: https://petl.readthedocs.io/en/latest/index.html
# For any datasource, regardless of type, self.data is an iterable data type
# that returns one tuple per row, where the first row are headers.

# To add additional extract/load functionality, simply extend the if statements
# to include a function that deals with the file type or database necessary.
# Check against petl's existing code base to make sure that there isn't an
# existing representation -- there likely is, it's pretty extensive.

# This code also includes basic utility functions and transform functions.

# To add transform functionality from petl, all that is needed is a quick
# translation of the desired petl function into this wrapper. If functionality
# that is not petl derived is required, it must be added here using the petl
# table object. petl tables are iterable, where each row returns as a tuple of
# values.

import csv
import sys
import petl
import os
# Add eblink directory to path
for root, dirs, files in os.walk('.'):
    if 'eblink.py' in files:
        sys.path.append(os.path.join(root))
import eblink as eb


# When you add a supported format, please add it to the SUPPORTED global for
# reference purposes, in the order added.

SUPPORTED = ['csv', 'pandas']

class UrbanETL():

    def __init__(self, datasource, datatype=None):
        self.datasource = datasource
        self.datatype = datatype
        self.data = None
        self.extract()

################################################################################
############################    Extract Function    ############################
################################################################################

    def extract(self):
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
                self.data = petl.io.fromdataframe(self.datasource,
                 include_index=False)
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

################################################################################
#############################    Load Function    ##############################
################################################################################


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


################################################################################
############################# Transform Functions ##############################
################################################################################

    def headers(self, extract):
        '''
        Returns the headers of the Extract table given as a tuple.
        '''
        return petl.util.base.header(extract.data)

    def link(self, data=[], how='eblink', interactive=False, links=[], uids=[],
     types=[], iterations=100000, alpha=1, beta=999, out='links'):
        '''
        Allows the user to carry out linking between mutliple datasets.
        '''
        files = [self.data] + [x.data for x in data]
        if how == 'eblink':
            if interactive == True:
                link = eb.EBlink(interactive=True, files=files)
            else:
                link = eb.EBlink(files=files)
                # Prepare inputs
                link._columns, link._matchcolumns = self._eblink_buildcols(
                 links)
                link._indices = uids
                link._column_types = self._eblink_buildtypes(link._columns[0],
                 types)
                link.iterations = iterations
                link.a = alpha
                link.b = beta
                # Carry out process
                link.build()
                link.model()
                link.build_crosswalk()

        if out == 'links':
            link.clean_tmp()
            return (link.crosswalk, link)

        if out == 'linked':
            link.clean_tmp()
            self.build_linked_data(link)

        if out == 'inter':
            link.clean_tmp()
            self.build_linked_data(link, interactive=True)


    def _eblink_buildtypes(self, columns, types):
        '''
        Private function for eblink. Builds dictionary for types input.
        '''
        rv = {}
        for i in range(len(columns)):
            rv[columns[i]] = types[i].upper()
        return rv

    def _eblink_buildcols(self, links):
        '''
        Private function for eblink. Builds column inputs from links.
        '''
        columns = [[] for x in links[0]]
        matchcolumns = {}
        for i in range(len(links)):
            for j in range(len(links[i])):
                columns[j].append(links[i][j])
                if j == 0:
                    matchcolumns[links[i][j]] = []
                else:
                    matchcolumns[columns[0][i]].append(links[i][j])
        return (columns, matchcolumns)

    def build_linked_data(self, link, interactive = False):
        '''
        Builds a linked dataset using data and a crosswalk. If
        interactive, will prompt user to choose a record to keep.
        Else, will choose only first file's record to keep.
        '''
        pass
