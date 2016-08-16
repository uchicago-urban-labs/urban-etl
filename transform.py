# UrbanETL Transform Functions
# 8/15/2016

# This file contains both wrappers for petl basic transformation functions as
# well as custom functions built specifically for the Urban Labs.

# To add additional functionality from petl, all that is needed is a quick
# translation of the desired petl function into this wrapper. If functionality
# that is not petl derived is required, it must be added here using the petl

import petl
import eblink

def headers(table):
    '''
    This function returns the headers of the Extract table given as a tuple.
    '''
    return petl.util.base.header(table)

def link(data=[], how='eblink', interactive=False, links=[], uids=[], types=[],
 iterations=100000, alpha=1, beta=999 out='pairs'):
    '''
    This function allows the user to carry out linking between mutliple
    datasets.

    Inputs: check Transform Functons file for more information.
    '''
    
