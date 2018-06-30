# Programs
This folder contains some programs along with their dependent files. Usage of the programs is described below.

# query.py
This command-line program is for general manipulation of the metadata database. It allows for (mostly) full control of the database.
<br />Basic usage of this program goes like this: <code>./query.py (table) (list of flags)</code> where (table) is the table to be 
used and (list of flags) can be anywhere from one flag to one of each, but must be at least one for proper usage.
<br /><u>Adding records into the database:</u><br />To add a record to a table, simply run the -a/--add flag <code>./query.py (table) -a name value (name value)</code>.
Additionally, to list all of the records in a table, use the -l/--list flag. An example is given below:<img src="../imgs/add.png" /><br />
Due to how the argument parsing works internally, specify the table before the -a/--add flag, otherwise it will interpret it as a part of a name-value pair.
<br /><u>Editing existing records:</u><br />To edit a record with the -e/--edit flag, specify the index of the record, the attribute to be changed, and the new value.
Generally, it is <code>./query.py (table) -e (index) (attribute) (newValue)</code>An example is given below:<img src="../imgs/edit.png" />
<br /><u>Searching the database:</u><br />

# gluex_metadb_cmd.py
This command-line program is used for easier manipulation of the DataSet table, allowing the user to create a DataSet and list all of them.

# datasets_webpage.py
This is a simple CherryPy application that displays the DataSet table, organized by its RunPeriod. It uses a built-in python webserver to serve the webpage.
To start it up, simply run <code>./datasets_webpage.py</code> and the webpage will be running. If running locally, it will be on localhost:8080.
