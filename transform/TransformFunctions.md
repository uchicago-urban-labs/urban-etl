## Transform Functions
This file contains in-depth descriptions for using UrbanETL transform functions.

##### `transform.headers(Extract)`
Returns the headers of the Extract table given as a tuple.
##### `transform.link(data=[], how='eblink', interactive=False, links=[], uids=[], types=[], iterations=100000, alpha=1, beta=999 out='pairs')`
Performs data linkage between multiple datasets.

__Arguments:__  
+ `data` is a list specifying Extract tables to link, e.g. `[Extract1, Extract2]`. Not all methods can take more than two datasets to link.
+ `how` specifies the method to use. Default is currently set to [ebLink](https://github.com/aldengolab/graphical-record-linkage). Other supported linkage methods include: ()
+ `interactive` will prompt the user for the needed information to carry out the data linkage when set to True. Some methods may require user input regardless of whether this is turned off.
+ `links` is a list of columns to link on, where each item is a tuple containing the name of the column in each subsequent Extract. For example, if Extract1 has a column 'column1' that contains the same information as 'col1' in Extract2, you would enter this in as the tuple `('column1', 'col1')` to link on those columns.
+ `uids` is a list of column names indicating the unique index in each Extract table, in order by
+ `out` specifies what to return:
  + `'pairs'` - default; an Extract object containing pairs of linked records
  + `'links'` - an Extract object containing only unique records; note that the function selects which record to keep
  + `'inter'` - interactively ask user to construct Extract object containing only unique records and return that object
+ *For ebLink:* `types` specifies whether each column is categorical (e.g. age, dates, census block) or a string to match (e.g. name, company). Must be a list, in order by `links`.
+ *For ebLink:* `iterations` is the number of Gibbs iterations to execute; 100,000 or more are recommended, with accuracy improving as the number increases.
+ *For ebLink:* `alpha` is the alpha value for the prior distribution for ebLink
+ *For ebLink:* `beta` is the beta value for the prior distribution for ebLink
