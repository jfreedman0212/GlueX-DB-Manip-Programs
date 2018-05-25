#!/usr/bin/env python

###############################################################################
# gluex_metadb_cmd.py -  A command line program that manipulates the DataSet  #
#			 table that also updates a webpage every time a       #
#			 DataSet is created or modified.		      #
# Written by Joshua Freedman						      #
###############################################################################

import DatabaseConnection as DBC
import argparse
import consts
import sys
import os

### useful variables and functions ###

## should probably refactor some of this (and -f flag too), but its fine for now ##

# generating a tuple to be used by the 'metavar' attribute of the create argument,
# will also be used in the actual create process
attributes = [a for a in dir(DBC.gluex_md.DataSet()) if not a.startswith('_') \
	      and a is not 'id'\
	      and not callable(getattr(DBC.gluex_md.DataSet(),a)) \
	      and a is not 'metadata' and 'Id' not in a]

# used to determine if an attribute is a reference to another table
tables = [item for item in dir(DBC.gluex_md) if not item.startswith('_') \
	  and 'DeclarativeMeta' in type(getattr(DBC.gluex_md,item)).__name__ \
	  and item is not 'DataSet' and item is not 'Base']

# function that creates a DataSet, used in create from command line and from file
def createDataSet(dbc,arguments):
	# dictionary that will contain the data needed to create the specified object
	addedAttrs = {}
	create = True
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
			
			if arg is 'NULL' and len(entry) == 0:
				create = False
				print 'Did not create DataSet because \"{0}\" is not a valid \"{1}\". Check \"{1}\" table.'.format(arg,attr)
				break
			elif len(entry) > 0:
				entryId = entry[0].id
				addedAttrs[attr + 'Id'] = entryId
	try:
		if create:
			dbc.create('DataSet',addedAttrs)
	except AttributeError as exc:
		print 'Something went wrong internally. Here is the error message:'
		print exc

# argparse setup
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')

parser.add_argument('-s', \
	metavar='DB_URL', \
	help='uses the specified URL instead of the environment variable')

parser.add_argument('-c', \
	metavar=tuple(attributes), \
	nargs=len(attributes), \
	help='creates a new DataSet with the specified values for each attribute of it')

parser.add_argument('-f', \
	metavar='pathToFile', \
	help='creates DataSets from a file, each line is in the format of the -c flag')

parser.add_argument('-d', \
	metavar=('DataType','RunPeriod','Revision'), \
	nargs=3, \
	help='deletes DataSets with the specified attributes')

parser.add_argument('-l','--list',action='store_true', \
	help='lists all of the DataSets in a user-friendly format')

args = parser.parse_args()

# ensures that at least ONE command line argument is given
if len(sys.argv) == 1:
	print 'Proper usage requires at least one argument. See options below:\n\n'
	parser.print_help()
	sys.exit(1)

# the DatabaseConnection object, will interact with the database
db = None

### procedures for the -s (change database URL) flag ###
try:
	if args.s is not None:
		db = DBC.DatabaseConnection(args.s)
	else:
		db = DBC.DatabaseConnection(os.environ[consts.DB_ENV_VAR])
except DBC.InvalidDatabaseURLException as exc:
	print exc
	sys.exit(1)
except KeyError:
	print 'Set the environment variable \"{}\" to a valid database URL.'.format(consts.DB_ENV_VAR)
	sys.exit(1)

### procedures for the -d (delete) flag ###
if args.d is not None:
	dataSets = db.search('DataType','name',args.d[0])[0].DataSets
	dataSets = list(set(dataSets).intersection(db.search('RunPeriod','name',args.d[1])[0].DataSets))
	dataSets = list(set(dataSets).intersection(db.search('DataSet','revision',args.d[2])))
	print 'Are you sure you want to delete the following DataSets?'
	for i in dataSets:
		print i
	
### procedures for the -c (create DataSet) flag ###
if args.c is not None:
	createDataSet(db,args.c)

### procedures for the -f flag ###
if args.f is not None:
	txt_file = None
	try:
		txt_file = open(args.f,'r')
	except IOError:
		print '\"{}\" does not exist.'.format(args.f)
	else:
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

### procedures for the -l,--list flag ###
if args.list:
	for entry in db.list_all('DataSet'):
		print entry
