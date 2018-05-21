#!/usr/bin/env python

###############################################################################
# DataSetManip.py - A command line program that manipulates the DataSet table #
#		    that also updates a webpage every time a new DataSet is   #
#		    created.						      #
# Written by Joshua Freedman						      #
###############################################################################

import DatabaseConnection as DBC
import argparse
import sys

### useful variables and functions ###

# generating a tuple to be used by the 'metavar' attribute of the create argument,
# will also be used in the actual create process
attributes = [a for a in dir(DBC.gluex_md.DataSet()) if not a.startswith('_') and a is not 'id'\
	      and not callable(getattr(DBC.gluex_md.DataSet(),a)) and a is not 'metadata' and 'Id' not in a]
# used to determine if an attribute is a reference to another table
tables = [item for item in dir(DBC.gluex_md) if not item.startswith('_') \
	  and 'DeclarativeMeta' in type(getattr(DBC.gluex_md,item)).__name__ \
	  and item is not 'DataSet' and item is not 'Base']

# function that creates a DataSet, used in create from command line and from file
def createDataSet(dbc,arguments):
	# dictionary that will contain the data needed to create the specified object
	addedAttrs = {}

	# generates the dictionary with corresponding attributes
	for attr,arg in zip(attributes,arguments):
		if attr not in tables:
			addedAttrs[attr] = arg
		else:
			entry = None
			try:
				entry = dbc.search(attr,'name',arg)
			except AttributeError:
				entry = dbc.search(attr,'value',arg)
			
			if len(entry) > 0:
				entryId = entry[0].id
				addedAttrs[attr + 'Id'] = entryId
	try:
		dbc.create('DataSet',addedAttrs)
	except AttributeError as exc:
		print 'Something went wrong internally. Here is the error message:'
		print exc

# argparse setup
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')
parser.add_argument('-s',metavar='DB_URL',help='uses the specified URL instead of the environment variable')
parser.add_argument('-c',metavar=tuple(attributes),nargs=len(attributes),help='creates a new DataSet with the specified values for each attribute of it')
parser.add_argument('-f',metavar='pathToFile',help='creates several DataSets from the specified file (file should be in format of -c flag)')
parser.add_argument('-l','--list',action='store_true',help='lists all of the DataSets in a user-friendly format')
args = parser.parse_args()

# the DatabaseConnection object, will interact with the database
db = None

# procedures for the -s (change database URL) flag
try:
	if args.s is not None:
		db = DBC.DatabaseConnection(args.s)
	else:
		db = DBC.DatabaseConnection(DBC.gluex_md.databaseEnv)
except DBC.InvalidDatabaseURLException as exc:
	print exc
	sys.exit(1)

# procedures for the -c (create DataSet) flag
if args.c is not None:
	createDataSet(db,args.c)

# procedures for the -f (create DataSets from file) flag
if args.f is not None:
	txt_file = open(args.f,'r')
	for line in txt_file.readlines():
		arguments = line.split(' ')
		# this for loop allows for entries to be specified with spaces as long as they
		# are surrounded by double quotes (")
		for string in arguments:
			if string.startswith('\"'):
				start = arguments.index(string)
				i = start + 1
				while True:
					# could be cleaned up, but works for now
					if not arguments[i].endswith('\"'):
						arguments[start] = arguments[start] + ' ' + arguments[i]
						arguments.pop(i)
					else:
						arguments[start] = arguments[start] + ' ' + arguments[i]
						arguments.pop(i)
						break
				arguments[start] = arguments[start].replace('\"','')
			if '\n' in string:
				arguments[arguments.index(string)] = arguments[arguments.index(string)].replace('\n','')
		createDataSet(db,arguments)
	txt_file.close()

#procedures for the -l,--list flag
if args.list:
	for entry in db.list_all('DataSet'):
		print entry
