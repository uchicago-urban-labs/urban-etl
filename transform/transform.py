# UrbanETL Transform Functions
# 8/15/2016

# This file contains both wrappers for petl basic transformation functions as
# well as custom functions built specifically for the Urban Labs.

# To add additional functionality from petl, all that is needed is a quick
# translation of the desired petl function into this wrapper. If functionality
# that is not petl derived is required, it must be added here using the petl
# table object. petl tables are iterable, where each row returns as a tuple of
# values.

import petl
import eblink as eb

def headers(table):
    '''
    Returns the headers of the Extract table given as a tuple.
    '''
    return petl.util.base.header(table)

def link(data=[], how='eblink', interactive=False, links=[], uids=[], types=[],
 iterations=100000, alpha=1, beta=999, out='links'):
    '''
    Allows the user to carry out linking between mutliple datasets.
    '''
    if how == 'eblink':
        if interactive == True:
            link = eb.EBlink(interactive=True, files=data)
        else:
            link = eb.EBlink(files=data)
            link._columns, link._matchcolumns = _eblink_buildcols(links)
            link._indices = uids
            link._column_types = types
            link.iterations = iterations
            link.a = alpha
            link.b = beta
            link.build()
            link.define()
            link.model()
            link.build_crosswalk()

    if out == 'links':
        return link.crosswalk

    if out == 'linked':
        build_linked_data(link)

    if out == 'inter':
        build_linked_data(link, interactive=True)

def _eblink_buildcols(links):
    '''
    Private function for eblink. Builds column inputs from links.
    '''
    columns = []
    matchcolumns = [[] for x in links[0][1:]]
    for link in links:
        columns.append(link[0])
        ind = 0
        for col in link:
            if ind != 0:
                matchcolumns[ind-1].append(col)
            ind += 1
    return (columns, matchcolumns)

def build_linked_data(link, interactive = False):
    '''
    Builds a linked dataset using data and a crosswalk. If
    interactive, will prompt user to choose a record to keep.
    Else, will choose only first file's record to keep.
    '''
