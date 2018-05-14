#!/usr/bin/env python

###############################################################################
# query.py - A command line program for creating, retrieving, updating, and   #
#	     retrieving data from the GlueX Metadata Database.		      # 
# Written by Joshua Freedman						      #
###############################################################################

import argparse
from pydoc import locate
from gluex_metadata_classes import * 


### should be updated to run DatabaseConnection object methods instead of what its currently doing ###
### update asap ###

# argparse setup
parser = argparse.ArgumentParser(description='Manipulates/retrieves data from the GlueX Metadata Database')
parser.add_argument('table',help='the table that will be manipulated/retrieved from')
parser.add_argument('-a',action='store_true',help='add the specified field to the specified table')
parser.add_argument('-e',nargs=3,help='edits the specified field from the specified table')
parser.add_argument('-d',type=int,help='deletes the specified index from the specified table')
parser.add_argument('-r',type=int,help='retrieves the record of the specified id from the specified table')
parser.add_argument('-v','--verbose',action='store_true',help='prints out each step of the specified process')
parser.add_argument('--version',action='version',version='Version 0.1')
args = parser.parse_args()

# run the add procedures
# POTENTIAL UPDATE: takes a variable amount of arguments so the user does not need to
# run the -a command and then the -e command to change it
if args.a:	
	session.add(globals()[args.table]())
	if args.verbose:
		print 'Added an empty field to the {} table.'.format(args.table)

# run the delete procedures
if args.d is not None:
	deletedRecord = session.query(locate('gluex_metadata_classes.' + args.table)).filter_by(id=int(args.d))
	if deletedRecord.first() is not None:
		if args.verbose:
			print 'Index {} of table {} deleted.'.format(args.d,args.table)	
		deletedRecord.delete()
	elif deletedRecord.first() is None and args.verbose:
		print 'There is no record at index {} for table {}'.format(args.d,args.table)		

# run the edit procedures
if args.e is not None:
	if args.verbose:
		print 'Index {} of table {} is being changed...'.format(args.e[0],args.table)
	editedRecord = session.query(locate('gluex_metadata_classes.'+args.table)).filter_by(id=int(args.e[0])).first()
	# for now this is fine, but it should be made to accomodate ANY type
	if type(getattr(editedRecord,args.e[1])) is unicode:
		setattr(editedRecord,args.e[1],args.e[2])
	elif type(getattr(editedRecord,args.e[1])) is int:
		setattr(editedRecord,args.e[1],int(args.e[2]))
	if args.verbose:
		print 'Index {} of table {} has the new value: {}'.format(args.e[0],args.table,editedRecord)

# run the retrieve procedures
# POTENTIAL UPDATE: -r takes a range as x,y and it prints out all records with ids in that range
if args.r is not None:
	"""for i in range(1,args.r):
		if i in range(1,session.query(locate('gluex_metadata_classes.'+args.table)).count()+1):
			print session.query(locate('gluex_metadata_classes.'+args.table)).filter_by(id=i).first()
		else:
			print 'End of table'
			break
	"""
	print session.query(locate('gluex_metadata_classes.'+args.table)).filter_by(id=args.r).first()	
# commits all changes at the end
# should there be a commit() during every function?
session.commit()
