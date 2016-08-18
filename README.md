# Urban ETL
A modular pipeline for extract-transform-load, created for the UChicago Urban Labs.

## Purpose
This code base is a flexible, easily extendible system for regularizing extract-transfer-load processes for the Urban Labs.
It provides general functions for data cleaning/de-duplication/linkage as well as specific functionalities based on the needs and practices at the labs.
Streaming lining the process will avoid reinventing the wheels and provide clarification and transparency on how data is being transformed.
Written in Python, this system can easily take new functions, either built off of petl (the underlying ETL code) or custom built for specific applications.

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


## Simple Usage
Urban ETL is designed to be as easy to use as possible:

`import urbanETL`

`table = urbanETL.extract('data.csv')`  
`table2 = urbanETL.extract('data2.json')`  
`table.normalize_dates('DOB')`  
`UrbanETL.normalize_dates(table2, 'dob')`  

`table_linked = transform.link([table, table2], how='eblink', links=[('DOB', 'dob'), ('NAME', 'fn'), ('SUR', 'ln')], uids=['ID', 'SSN'], types=['c', 's', 's'], iterations=100000, alpha=1, beta=999 out='linked')`

`table_linked.load('linked.csv')`
