#!/usr/bin/env python

###############################################################################
# gluex_metadb_cmd.py -  A command line program that manipulates the DataSet  #
#			 table that also updates a webpage every time a				      #
#			 DataSet is created or modified.							      #
# Written by Joshua Freedman											      #
###############################################################################

from gluex_metadb_utils import databaseconnection as DBC
from gluex_metadb_utils import constants as consts
from gluex_metadb_utils.metadatamodel import DataSet
import argparse
import sys
import os

# function that creates a DataSet, used in create from command line and from file
def createDataSet(dbc,arguments):
	# dictionary that will contain the data needed to create the specified object
	addedAttrs = {}
	create = True
	# generates the dictionary with corresponding attributes
	for attr,arg in zip(dbc.get_attributes('DataSet'),arguments):
		try:
			getattr(DataSet, attr + 'Id')
		except AttributeError:			
			addedAttrs[attr] = arg
		else:
			entry = None
			if attr in dbc.get_tables():
				try:
					entry = dbc.search(attr,'name',arg)
				except AttributeError:
					entry = dbc.search(attr,'value',arg)
			else:
					entry = dbc.search('DataSet','nickname',arg)
			# valid entries include: 'NULL' or something that is part of the specified table
			if arg == 'NULL':
				continue		
			elif len(entry) == 0:
				create = False
				print 'Did not create DataSet because "{0}" is not a valid "{1}". Check "{1}" table.'.format(arg,attr)
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

### argparse setup ###
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')

parser.add_argument('-s','--set-url', 
	metavar='DB_URL', 
	help='uses the specified URL instead of the environment variable')

parser.add_argument('-c','--create', 
	metavar=tuple(DBC.DatabaseConnection.get_attributes('DataSet')), 
	nargs=len(DBC.DatabaseConnection.get_attributes('DataSet')), 
	help='creates a new DataSet with the specified values for each attribute of it')

parser.add_argument('-f','--from-file', 
	metavar='pathToFile', 
	help='creates DataSets from a file, each line is in the format of the -c flag')

parser.add_argument('-d','--delete', 
	metavar=('DataType','RunPeriod','Revision'), 
	nargs=3, 
	help='deletes DataSets with the specified attributes')

parser.add_argument('-l','--list',action='store_true', 
	help='lists all of the DataSets in a user-friendly format')

args = parser.parse_args()

# ensures that at least ONE command line argument is given
if len(sys.argv) == 1:
	print 'Proper usage requires at least one argument. See options below:\n\n'
	parser.print_help()
	sys.exit(1)

### procedures for the -s (change database URL) flag ###
try:
	if args.set_url is not None:
		db = DBC.DatabaseConnection(args.set_url)
	else:
		db = DBC.DatabaseConnection(os.environ[consts.DB_ENV_VAR])
except DBC.InvalidDatabaseURLException as exc:
	print exc
	sys.exit(1)
except KeyError:
	print 'Set the environment variable "{}" to a valid database URL.'.format(consts.DB_ENV_VAR)
	sys.exit(1)

### procedures for the -d (delete) flag ###
if args.delete is not None:
	dataSets = set(db.search('DataType','name',args.delete[0])[0].DataSets)
	dataSets = dataSets.intersection(db.search('RunPeriod','name',args.delete[1])[0].DataSets)
	dataSets = dataSets.intersection(db.search('DataSet','revision',args.delete[2]))

	if dataSets:
		print 'Are you sure you want to delete the following DataSets? (Y/N)'
		for i in dataSets:
			print i
		answer = raw_input()
		if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'Yes':
			for dataset in dataSets:
				db.remove('DataSet',dataset.id)
		else:
			print 'Did not delete these DataSets'
	else:
		print 'There were no DataSets that met this criteria'

### procedures for the -c (create DataSet) flag ###
if args.create is not None:
	createDataSet(db,args.create)

### procedures for the -f flag ###
if args.from_file is not None:
	try:
		txt_file = open(args.from_file,'r')
	except IOError:
		print '"{}" does not exist.'.format(args.from_file)
	else:
		for line in txt_file.readlines():
			arguments = line.split(' ')
			# this for loop allows for entries to be specified with spaces as long as they
			# are surrounded by double quotes (")
			for string in arguments:
				if string.startswith('"'):
					start = arguments.index(string)
					i = start + 1
					while True:
						# could be cleaned up, but works for now
						if not arguments[i].endswith('"'):
							arguments[start] = arguments[start] + ' ' + arguments[i]
							arguments.pop(i)
						else:
							arguments[start] = arguments[start] + ' ' + arguments[i]
							arguments.pop(i)
							break
					arguments[start] = arguments[start].replace('"','')
				if '\n' in string:
					arguments[arguments.index(string)] = arguments[arguments.index(string)].replace('\n','')
			createDataSet(db,arguments)
		txt_file.close()

### procedures for the -l,--list flag ###
if args.list:
	if db.list_all('DataSet'):
		for entry in db.list_all('DataSet'):
			print entry
	else:
		print 'There are no DataSets'
