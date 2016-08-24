# Urban ETL
A modular pipeline for extract-transform-load, created for the UChicago Urban
Labs.

## Purpose
This code base is a flexible, easily extensible system for regularizing extract-transfer-load processes for the Urban Labs. It provides general functions for data cleaning/de-duplication/linkage as well as specific functionalities based on the needs and practices at the labs. Streamlining the process will avoid constant re-coding and provide clarification and transparency on how data is being transformed. Written in Python, this system can easily take new functions, either built off of petl (the underlying ETL code) or custom built for specific applications.

## Requirements
This code is written in Python 2.7. Make sure the run the requirements.txt file for the necessary packages outside of this repo:
+ [petl](https://petl.readthedocs.io) - for which Urban ETL is primarily a simple-to-use wrapper
+ [pandas](http://pandas.pydata.org/pandas-docs/version/0.15.2/index.html) - for which Urban ETL is primarily a simple-to-use wrapper
+ [sqlalchemy](https://readthedocs.org/projects/sqlalchemy/) - which allows Extracts and Loads to SQL databases
+ [ebLink for Python](https://github.com/aldengolab/graphical-record-linkage) - which is a Python encapsulation of [ebLink](https://github.com/resteorts/ebLink), contained within this directory

## Supported Input/Output File Types:
+ Excel: .xls/.xlrd/.xlwt/.xlsx
+ .dta
+ .csv
+ .json
+ .html
+ dataframes (pandas)
+ pickle file
+ databases .db

## Sample Usage

Urban ETL is designed to be as easy to use as possible for a non-Python user:

`import UrbanETL as ub`

`table = ub.UrbanETL('data.csv')`  
`table2 = ub.UrbanETL('data2.json')`  
`table.normalize_dob('DOB')`  
`table2.normalize_dob('dob')`  

`table_linked = transform.link([table, table2], how='eblink', links=[('DOB', 'dob'), ('NAME', 'fn'), ('SUR', 'ln')], uids=['ID', 'PIN'], types=['c', 's', 's'], iterations=100000, alpha=1, beta=999 out='linked')`

`table_linked.load('linked.csv')`

## Manual

The manual containing all current functions and their options is contained in
`manual.md`.

Functionality falls under three headings:
+ Extract Functions - called when initializing the class
+ Utility Functions - perform standard peek, head, foot functions
+ Transform Functions - edit the table in place
+ Load Functions - will load the table into a specified destination

## Extension

This ETL pipeline is built to be easily extensible. If a function is needed or
wanted but not included, first check whether it is offered by the [petl](https://petl.readthedocs.io)
existing functionality; if not, custom functions are easily added. Please take
a look at existing code to get an understanding of how functionality works.

Generally, new functions should be built into the main UrbanETL class contained
in `urbanetl.py` and follow the form:

`tablename.functionname('column', inplace = True, **kargs)`

The `self._data` attribute is a `petl` object containing the data and has all
the related functionality. This includes
[iteration](https://petl.readthedocs.io/en/latest/intro.html#petl-executable),
[map, and  sort](https://petl.readthedocs.io/en/latest/transform.html#transforming-rows),
methods, which are probably the most commonly needed functionality.

**All functions doing transforms should make edits in place by default**.
Note that petl does *not* make edits in place. As such, before returning,
functions within the class will need to have an option to set `inplace = False`
explicitly when using petl.

If any code extension is in progress, please branch this repo into a development
branch for yourself and request a merge pull, rather than developing directly
in this master. While this goes without saying for most developers, do keep in
mind that this product will be used by a variety of audiences.

Once a custom function is complete and tested, please add the full description
to `manual.md`.

## Contact

To raise issues or request development, please use the Issues tab. Current
owners are:

+ [Owen McCarthy](https://github.com/OwenMcCarthy) - Urban Poverty Lab, Chicago
+ [Lingwei Cheng](https://github.com/lw334) - Urban Poverty Lab, Chicago

This codebase was originally developed by [Alden Golab](https://www.github.com/aldengolab).
