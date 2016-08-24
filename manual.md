# Urban ETL Manual

This manual contains full descriptions for the functionality of Urban ETL.

**Supported Extract/Load Data Types:**  
+ `'csv'` - a csv text file
+ `'pandas'` - a Pandas dataframe objects

Throughout this manual, we refer to the UrbanETL object as a table.

## Initialize

To initialize an instance of UrbanETL, use the following code:

`import urbanetl as ub`  
`table = ub.UrbanETL('datasource', datatype = 'type')`

+ `datasource` should be a file or database object
+ `datatype` isn't always necessary; Urban ETL will do its best to figure out
  what kind of datasource has been entered. Accepted file types are listed above.

## Extract
There is only one extract function, called when the UrbanETL class is initialized:

### `table.extract(datasource, datatype='')`

+ If called outside of the initialization, this function will override the existing
  data in the table if called. Currently supported file types are listed above.
  If edited to include more, please make sure to add above and to the SUPPORTED
  global in the code.
 + `datasource` should be a file or database object
 + `datatype` isn't always necessary; Urban ETL will do its best to figure out
  what kind of datasource has been entered. Accepted file types are listed above.

## Load
There is only one load function, which much be called explicitly:

### `table.load('destination', dest_type = 'csv')`

+ Built to understand a variety of destination types. Currently
supported file types are listed above. If edited to include more, please make
sure to add above and to the SUPPORTED global in the code.
 + `datasource` should be a file or database object
 + `datatype` isn't always necessary; Urban ETL will do its best to figure out
 what kind of datasource has been entered. Accepted file types are listed above.

## Utilities
Utility functions are used to perform tasks that don't make edits to data, like
head or get column names.

### `table.headers()`

+ Returns the headers/column names of the table as a list.

### `table.get(index, 'column')`

+ Returns an individual entry from the table based on its index for the column
  specified. Entry value MUST be unique, else returns the first entry found for
  that value.

## Transform
Transform functions directly edit the table contained within the UrbanETL class
object.

### `table.link(data=[table2, table3], how='eblink', interactive=False, links=[], uids=[], types=[], iterations=100000, alpha=1, beta=999 out='pairs')`

+ Performs data linkage between multiple datasets.

__Arguments:__  
+ `data` is a list specifying Extract tables to link, e.g. `[Extract1, Extract2]`. Not
  all methods can take more than two datasets to link.
+ `how` specifies the method to use. Default is currently set to
  [ebLink](https://github.com/aldengolab/graphical-record-linkage). Other supported
  linkage methods include: ()
+ `interactive` will prompt the user for the needed information to carry out the data
  linkage when set to True. Some methods may require user input regardless of whether
  this is turned off.
+ `links` is a list of columns to link on, where each item is a tuple containing the
  name of the column in each subsequent Extract. For example, if Extract1 has a column
  'column1' that contains the same information as 'col1' in Extract2, you would enter
  this in as the tuple `('column1', 'col1')` to link on those columns.
+ `uids` is a list of column names indicating the unique index in each Extract table,
  in order by
+ `out` specifies what to return:
  + `'links'` - default; an Extract object containing pairs of linked records with only their UIDs specified
  + `'linked'` - an Extract object containing only unique records; note that the function selects the first file's record to keep, dropping other files' records
  + `'inter'` - interactively ask user to construct Extract object containing only unique records and return that object
+ *For ebLink:* `types` specifies whether each column is categorical (e.g. age, dates, census block) or a string to match (e.g. name, company). Must be a list, in order by `links`.
+ *For ebLink:* `iterations` is the number of Gibbs iterations to execute; 100,000 or more are recommended, with accuracy improving as the number increases.
+ *For ebLink:* `alpha` is the alpha value for the prior distribution for ebLink.
+ *For ebLink:* `beta` is the beta value for the prior distribution for ebLink.
