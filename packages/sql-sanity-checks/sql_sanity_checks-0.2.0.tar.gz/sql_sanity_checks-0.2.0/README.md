# SQL Sanity Check

A Python Library to help perform tests on SQL engines to assess the quality of the data.

Created by Jose Santos  
[josemrsantos@gmail.com](mailto:josemrsantos@gmail.com)  
[https://www.linkedin.com/in/josemrsantos/](https://www.linkedin.com/in/josemrsantos/)

## Why ?
Because sometimes we need to make sure that the data we have is correct. This is especially true when we have a lot of
data, and we are not sure if the data is correct. This library is a simple way to create tests that can be run on a SQL
engine to make sure that the data is correct.  

Also very useful for when you have an orchestrator (e.g. airflow) and want to automate some SQL tests that you might 
already have.

## How to install it

The library is already available on PyPi, so you can install it with pip: `pip install sql_sanity_check`  
Another option is to clone the repository and install it with pip: `pip install .`  
Finally, this code does have a MIT license, so cloning it to an internal repository is also a valid option. There new 
classes can be added and the code can be modified to suit your needs.

## How to run it
This package comes with a demo script called sq_sanity_check_demo.py. This script will run a few tests on the
Chinook.db database that is included in the demo directory. The script will run a few tests and output the results to
stdout. The script can be run with the following command: `python sql_sanity_check_demo.py`.
*`Please crease a similar script to run your own tests. To use the sqlite connector, this cou`*ld be as simple as:

```python
import sanity_checks
import connector_sqlite  # or any other connector

# import custom_output # or use the default output class
db_path = "./demo/Chinook.db"  # Adjust the path as necessary
tests_path = "./sql_tests/"  # Adjust the path as necessary
db_connector = connector_sqlite.SQLiteDBConnector(db_path)
sanity_checks.SanityCheck(tests_path=tests_path, connector=db_connector)
```


## How it works

It could not be more simple: Create SQL code that returns rows if you want the test to fail.

### A more intuitive way to look at these SQL tests

A bit more information is probably needed, because "return rows if you want the test to fail", sounds a bit counter-intuitive. To make a bit more "intuitive", imagine that you have a table (**TableA**) that is the source, then you need to make a Transformation (**T1**) that outputs into the destination table (**TableB**). Given that **T1** might become quite complex, we want to make sure every time an update happens to **TableA** , that gets refletcted in **TableB**. A "simple test" would be to check if **TableB** has the same ids as **TableA** (for the sake of keeping it simple, we are assuming that **T1** transfers a column **TrackId** from **TableA** to **TableB** as is). The test could look something like this:

```
SELECT ta.TrackIdasmissing_id
FROM TableA ta
LEFT JOIN TableB tb ON ta.TrackId=tb.TrackId
WHERE tb.TrackId IS NULL;
```

*These 2 tables actually exist in the demo DB Chinook.db and are both created from the table **Track**. A SQK test case with that exact code is also included in the sql_tests directory.*

### Some Details

You create individual SQL queries that you place in .sql files, inside a directory (look at the sql_tests directory for a few examples).

The library will run all SQL files inside the specified directory, and will fail with an exception if any of the tests fail. The name of the file, its contents and the values returned are also given to the output_objects.

A default output_object is already included that only outputs to stdout (any log call) or to stderr (any error call)

### Anatomy of a connector

A connector is an independent Python module that takes care of the connection to a specific SQL DB engine.
The Class created needs to be a context manager so that it can be used with the with statement. In the Library this class will be called something like:

```python

with self.connector as conn:
    result = conn.execute_query(sql_code)
```

The following methods should be implemented to the class:  
**connect**: Method that creates a connection to the DB  
**execute_query**: Method that send a SQL command to the server and returns the result as an iterator  
**close**: Method that closes a connection to the DB  
`__enter__` and `__exit__`: So that the class is a content manager.  

Looking at the module connector_sqlite.py might also help.

Specific connectors can be created and passed to the creation of the SQLSanityCheck object. 
The default connector is the SQLite connector and there can be only one connector (queries are only done in one server).


### Anatomy of an output

An output class should define where the output of either a log or an error should go. 
The default output is the StdOutErrOutput class that outputs to stdout and stderr. 
The class should have the following methods:  
**log**: Method that logs a message, based on the input parameters   
**error**: Method that logos an error message, based on the input parameters.  
Both methods should have the input parameters: **test_name**, **test_result** and **code**. 
They should based on those parameters be able to create a valid message.  
**IMPORTANT:** **test_result** will be [] if no rows are returned by the SQL query and will be None if the library is
only sending the message that the test **test_name**.  
The creation of an object with SanityCheck accepts in the output_objects parameter a list of output objects.
This means that the output can be sent to multiple places.

## SQL tests code examples
### Simple tests
A few simple tests have already been included in the sql_tests directory and these work around checking different 
values on different tables. Counting the number of lines might also be a simple and effective test. eg:

```sql
WITH table_track AS (SELECT count(*) AS count_t FROM Track),
     table_invoiceline AS (SELECT count(DISTINCT TrackId) AS count_il FROM InvoiceLine)
SELECT count_t, count_il
FROM table_track, table_invoiceline
WHERE count_t < count_il;
```
The previous test only checks if we don't have more distinct TrackIds on the table **InvoiceLine** than the number of 
actual Tracks in tha table **Track**.

### Tests on foreign data

This is very specific and it is more related with good writing good SQL. Several DB servers are offering some sort of 
"foreign data access". A few examples are the FDW on PostgreSQL that allows one PostgreSQL server to have access to 
tables that are on a different server. The main caveat of this, is that any query that is done on the server that only 
has the "foreign table" that itself is in a second server, the actual query will be done on the "second server".

#### An example:

**ServerA** has 2 tables: **table_a_1** and **table_a_2**. **ServerB** has only 1 table: **table_b_1**, but it also has 
a FDW connection to ServerA, so it also "allows queries" on those tables.

If we do a SELECT on **ServerB** such as `SELECT name FROM table_a_1 LIMIT 10`, that query will run on **ServerA** and 
return the result (using the network) to **serverB**. This is not a problem, because it is all running on the same 
server (in this case **ServerA**) and the volume of data going through the network is not very large. This is just a 
simple example, but Redshift also has some similar capabilities as well as other capabilities, where this is not an 
issue. If you use any sort of "data sharing", please check the DB server that you are using. if this might something 
you need to consider.

When we have a case where we make a query to ServerB that might send a part or all the query to ServerA, the general 
advice would be to keep it as separate as possible and minimise possible network usage (e.g. using CTEs).

A good example of keeping to these rules, has already been given before. Lets say that we have **Track** and 
**InvoiceLine** on different servers. Using CTEs and fetching a low number of rows/data is a good way to create a SQL 
test (please see the previous code example).

## Existing connectors
### SQLite
The SQLite connector is already included in the library. This connector is very simple and only needs the path to the
database file. The connector will create a connection to the database and will close it when the context manager is
exited. The connector will also execute the SQL code and return the result as an iterator.
A few tests have already been included in the sql_tests/sqlite directory that work with the Chinook.db database that is 
also included in the demo directory.

### PostgreSQL
The PostgreSQL connector is also included in the library. This connector is a bit more complex than the SQLite connector
because it needs the connection parameters to the database. The connector will create a connection to the database and
will close it when the context manager is exited. The connector will also execute the SQL code and return the result as
an iterator.
A few tests have already been included in the sql_tests/postgresql directory that work with the Chinook_PostgreSql.sql 
dataset that is also included in the demo directory.
#### How to load the dataset into a PostgreSQL server
To load the dataset into a locally running PostgreSQL server, you can use the following command:
```bash
psql -U postgres -a -f demo/Chinook_PostgreSql.sql
```
This command will load the dataset into the database that is running on the default port on the localhost. The user
postgres is used to connect to the database. The password for the user postgres is not set, so no password is needed.
The dataset will be loaded into a database called chinook.

#### Testing the PostgreSQL connector
To test the PostgreSQL connector, you can use the following code:
```python
import connector_postgresql
import sanity_checks
import custom_output
db_params = {
    "host": "localhost",
    "port": 5432,
    "database": "chinook",
    "user": "postgres
}
db_connector = connector_postgresql.PostgreSQLConnector(db_params)
output = custom_output.CustomOutput()
sanity_checks.SanityCheck(tests_path="./sql_tests/PostgreSQL/", connector=db_connector, output_objects=[output])
```
A script called sql_sanity_check_postgresql_demo.py is also included. This script will run the tests in the
sql_tests/PostgreSQL directory and will output the results to stdout.

## Usage and contributions

The code (as simple as it is), is released under the MIT license, that AFAIK is one of the most (if not the most) 
permissive license. So, please use it as you wish and get in touch if you need anything, but don't blame me if 
something goes wrong.

In terms of contributions, I would be very happy to accept anything you can contribute with. From small fixes to this 
Readme to adding other connectors and output classes that could help others.
