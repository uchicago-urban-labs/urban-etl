# Urban ETL
A modular pipeline for extract-transform-load, created for the UChicago Urban Labs.

## Purpose
This code base is a flexible, easily extendible system for regularizing extract-transfer-load processes for the Urban Labs. Written in Python, this system can easily take new functions, either built off of petl (the underlying ETL code) or custom built for specific applications. 

## Requirements
This code is written in Python 2.7. Make sure the run the requirements.txt file for the necessary packages outside of this repo: 
+ [petl](petl.readthedocs.io) - for which Urban ETL is primarily a simple-to-use wrapper
+ [sqlalchemy](https://readthedocs.org/projects/sqlalchemy/) - which allows Extracts and Loads to SQL databases

## Simple Usage
Urban ETL is designed to be as easy to use as possible: 

`import UrbanETL`

`table = UrbanETL.Extract('data.csv')`  
`table2 = UrbanETL.Extract('data2.json')`  
`UrbanETL.normalize_dates(table, 'DOB')`  
`UrbanETL.normalize_dates(table2, 'dob')`  

`table_linked = transform.link([table, table2], how='eblink', links=[('DOB', 'dob'), ('NAME', 'fn'), ('SUR', 'ln')], uids=['ID', 'SSN'], types=['c', 's', 's'], iterations=100000, alpha=1, beta=999 out='linked')`

`table_linked.load('linked.csv')`
