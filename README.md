# Urban ETL
A modular pipeline for extract-transform-load, created for the UChicago Urban Labs.

## Purpose
This code base is a flexible, easily extendible system for regularizing extract-transfer-load processes for the Urban Labs. Written in Python, this system can easily take new functions, either built off of petl (the underlying ETL code) or custom built for specific applications.

## Requirements
This code is written in Python 2.7. Make sure the run the requirements.txt file for the necessary packages outside of this repo:
+ [petl](https://petl.readthedocs.io) - for which Urban ETL is primarily a simple-to-use wrapper
+ [sqlalchemy](https://readthedocs.org/projects/sqlalchemy/) - which allows Extracts and Loads to SQL databases
+ [ebLink for Python](https://github.com/aldengolab/graphical-record-linkage) - which is a Python encapsulation of [ebLink](https://github.com/resteorts/ebLink), contained within this directory

## Sample Usage

Urban ETL is designed to be as easy to use as possible:

`import UrbanETL as ub`

`table = ub.UrbanETL('data.csv')`  
`table2 = ub.UrbanETL('data2.json')`  
`table.normalize_dob('DOB')`  
`table2.normalize_dob('dob')`  

`table_linked = transform.link([table, table2], how='eblink', links=[('DOB', 'dob'), ('NAME', 'fn'), ('SUR', 'ln')], uids=['ID', 'PIN'], types=['c', 's', 's'], iterations=100000, alpha=1, beta=999 out='linked')`

`table_linked.load('linked.csv')`

## Manuals

The manual containing all current functions and their options is contained in `Functions.md`.
