# query.py
A command line program that manipulates the GlueX Metadata Database using SQLAlchemy.
The schema of the database is laid out in the "gluex_metadata_classes.py" file.
# how to use it
./query.py <tablename> <flags>

[tablename] is the name of the table being manipulated
<flags> are:
	-a: adds an empty field to the table
	-e <index> <attrChanged> <newValue> changes the record's <attrChanged> attribute at index <index> to <newValue>.
	-d <index>: deletes the record from the table at index <index>
	-r <index>: prints out the record at index <index>
	-h,--help: prints out help
	-v,--verbose: prints out more information
	--version: prints the version number
