# GlueX Metadata Database Manipulation Programs
This repo contains some programs that manipulate the GlueX Metadata Database. They are described below. 
These programs use an environment variable that shows the path to the database file. So, if using bash for example, put this in your .bashrc or .bash_profile before using:
<code>export GLUEX_DB="path to database file"</code>
where "path to database file" would be changed to the path of the file.

If you want to change the name of the environment variable, change the name of DB_ENV_VAR in consts.py to the desired name.

# query.py
A command line program that manipulates the GlueX Metadata Database using SQLAlchemy.
The schema of the database is laid out in the "gluex_metadata_classes.py" file.

Usage:

./query.py tablename flags

"tablename" is the name of the table being manipulated

flags are:

	-a: adds an empty field to the table

	-e <index> <attrChanged> <newValue>: changes the record's <attrChanged> attribute at index <index> to <newValue>.

	-d <index>: deletes the record from the table at index <index>

	-r <index>: prints out the record at index <index>

	-h,--help: prints out help

	-v,--verbose: prints out more information

	--version: prints the version number

# DataSetManip.py
!!! edit this when done with the first version of DataSetManip.py !!!
