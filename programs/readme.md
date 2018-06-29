#Programs
This folder contains some programs along with their dependent files. Usage of the programs is described below.

#query.py
This command-line program is for general manipulation of the metadata database. It allows for (mostly) full control of the database.
<br />Basic usage of this program goes like this: <code>./query.py (table) (list of flags)</code> where (table) is the table to be 
used and (list of flags) can be anywhere from one flag to all of them, but must be at least one for proper usage.


#gluex_metadb_cmd.py
This command-line program is used for easier manipulation of the DataSet table, allowing the user to create a DataSet and list all of them.

#datasets_webpage.py
This is a simple CherryPy application that displays the DataSet table, organized by its RunPeriod. It uses a built-in python webserver to serve the webpage.
To start it up, simply run <code>./datasets_webpage.py</code> and the webpage will be running. If running locally, it will be on localhost:8080.
