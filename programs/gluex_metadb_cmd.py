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

# generating a tuple to be used by the 'metavar' attribute of the create argument,
# will also be used in the actual create process
attributes = [a for a in dir(DBC.gluex_md.DataSet()) if not a.startswith('_') and a is not 'id'\
	      and not callable(getattr(DBC.gluex_md.DataSet(),a)) and a is not 'metadata' and 'Id' not in a]
tables = [item for item in dir(DBC.gluex_md) if not item.startswith('_') \
	  and 'DeclarativeMeta' in type(getattr(DBC.gluex_md,item)).__name__ \
	  and item is not 'DataSet' and item is not 'Base']

# argparse setup
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')
parser.add_argument('-s',metavar='DB_URL',help='uses the specified URL instead of the environment variable')
parser.add_argument('-c',metavar=tuple(attributes),nargs=len(attributes),help='creates a new DataSet with the specified values for each attribute of it')
parser.add_argument('-f',metavar='pathToFile',help='creates several DataSets from the specified file (file should be in format of -c flag)')
parser.add_argument('-l','--list',action='store_true',help='lists all of the DataSets in a user-friendly format')
parser.add_argument('-v','--verbose',action='store_true',help='makes output more descriptive')
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
	# dictionary that will contain the data needed to create the specified object
	addedAttrs = {}

	# generates the dictionary with corresponding attributes
	for attr,arg in zip(attributes,args.c):
		if attr not in tables:
			addedAttrs[attr] = arg
		else:
			entry = None
			try:
				entry = db.search(attr,'name',arg)
			except AttributeError:
				entry = db.search(attr,'value',arg)
		
			entryId = entry[0].id
			addedAttrs[attr + 'Id'] = entryId
	try:
		db.create('DataSet',addedAttrs)
	except AttributeError as exc:
		print 'Something went wrong internally. Here is the error message:'
		print exc

# procedures for the -f (create DataSets from file) flag
if args.f is not None:
	pass

#procedures for the -l,--list flag
if args.list:
	for entry in db.list_all('DataSet'):
		print entry
