# UrbanETL
# 8/15/2016

# This file is a wrapper for petl unctions. There is very
# little structure to this code; it essentially determines from the input string
# what kind of extract strategy to execute, unless specified by the user.

# petl documentation: https://petl.readthedocs.io/en/latest/index.html
# For any datasource, regardless of type, self._data is an iterable data type
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

class UrbanETL(object):

    def __init__(self, datasource, datatype=None):
        self._datasource = datasource
        self._datatype = datatype
        self._data = None
        self.extract()

################################################################################
############################    Extract Function    ############################
################################################################################

    def extract(self):
        '''
        A nest of booleans to determine which extract function to call.

        See the SUPPORTED global for currently supported file types.
        '''
        if self._datatype == 'csv' or '.csv' in self._datasource:
            ### CSV ###
            try:
                self._data = petl.io.fromcsv(self._datasource)
                if 'failed' not in self._data:
                    print "----> Data extracted successfully."
                    return
                else:
                    print "----> ERROR: Cannot read csv file."
            except Exception as e:
                print "----> ERROR: Cannot read csv file. {}".format(e)
        if self._datatype == 'pandas':
            ### PANDAS ###
            try:
                self._data = petl.io.fromdataframe(self._datasource,
                 include_index=False)
                if 'failed' not in self._data:
                    print "----> Data extracted successfully."
                    return
                else:
                    print "----> ERROR: Cannot read pandas dataframe."
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
            petl.io.csv.tocsv(self._data, destination, **kargs)
            print "----> Data written to {}.".format(destination)

        ### PANDAS ###
        if desttype == 'pandas':
            # Additional arguments:
            #   index=None, exclude=None, columns=None, coerce_float=False, nrows=None
            return petl.io.pandas.todataframe(self._data, **kargs)

        ### ERROR MESSAGE ###
        else:
            print "----> This destination type is not yet supported."
            print "----> Urban ETL currently supports the following data formats:\n"
            for x in SUPPORTED:
                print "        {}".format(x)

################################################################################
#############################  Utility Functions  ##############################
################################################################################

    def headers(self):
        '''
        Returns the headers of the Extract table given as a tuple.
        '''
        return petl.util.base.header(self._data)

################################################################################
############################# Transform Functions ##############################
################################################################################

## Transform functions should always operate inplace by default.
## Note that this requires editing the self._data table directly; petl functions
## do not edit in place.

    def link(self, data=[], how='eblink', interactive=False, links=[], uids=[],
     types=[], iterations=100000, alpha=1, beta=999, out='links'):
        '''
        Allows the user to carry out linking between mutliple datasets.

        Note that this function uses pandas in the build_crosswalk call, and
        thus may have performance problems at scale.
        '''
        files = [self._data] + [x._data for x in data]
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
            # Outputs the crosswalk of UIDs for each file
            link.clean_tmp()
            return UrbanETL(link.crosswalk, 'pandas')

        if out == 'linked':
            # Outputs the linked file with the columns used in the link
            # Non-interactive, will select first entry
            link.build_linked_data()
            link.clean_tmp()
            return UrbanETL(link.linked_set, 'pandas')

        if out == 'inter':
            # Interactively asks which linked entries to keep
            link.build_linked_data(interactive=True)
            link.clean_tmp()
            return UrbanETL(link.linked_set, 'pandas')

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

    def get(self, index, column):
        '''
        Gets an individual entry from the UrbanETL object based on its index.
        Entry value MUST be unique, else returns the first entry found for
        that value.
        '''
        try:
            lkp = petl.lookupone(self._data, column, strict=True)
            return list(lkp[str(index)])
        except petl.errors.DuplicateKeyError as e:
            print e

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(petl.util.vis.look(self._data, style='minimal'))

    def __iter__(self):
        for x in self._data:
            yield x

    def __len__(self):
        return len(self._data)
