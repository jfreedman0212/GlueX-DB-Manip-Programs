#!/usr/bin/env python

###############################################################################
# DataSetManip.py - A command line program that manipulates the DataSet table #
#		    that also updates a webpage every time a new DataSet is   #
#		    created.						      #
# Written by Joshua Freedman						      #
###############################################################################

# import dependencies
import argparse
from gluex_metadata_classes import * 

# argparse setup
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')
parser.add_argument('-s',metavar='pathToDB',help='changes the environment variable for the DB file to the specified pathname')
parser.add_argument('-c',metavar=('nickName','dataType','revision','runPeriod','softwareVersion','janaConfig','janaCalibContext'),\
		    nargs=7,help='creates a new DataSet with the specified values for each attribute of it')
parser.add_argument('-f',metavar='pathToFile',help='creates several DataSets from the specified file (file should be in format of -c flag)')
parser.add_argument('-l','--list',action='store_true',help='lists all of the DataSets in a user-friendly format')
parser.add_argument('-v','--verbose',action='store_true',help='makes output more descriptive')
args = parser.parse_args()

# runs the modification procedures first, then the display procedure 
# if a modification and a display flag are both called

# procedures for the -s (set env var) flag
if args.s is not None:
	if os.path.isfile(args.s) and '.db' in args.s:
		if args.verbose:
			print 'Old value: {}'.format(os.environ[consts.DB_ENV_VAR])
		os.environ[consts.DB_ENV_VAR] = args.s
		if args.verbose:
			print 'New value: {}'.format(os.environ[consts.DB_ENV_VAR])
	elif args.verbose:
		print '{} does not exist, try again.'.format(args.s)

	# next step: change the env variable permanently AND change the db for SQLAlchemy

# procedures for the -c (create DataSet) flag
if args.c is not None:
	dataTypeIndex = session.query(DataType).filter_by(name=args.c[1]).first().id
	runPeriodIndex = session.query(RunPeriod).filter_by(name=args.c[3]).first().id
	softwareVersId = session.query(SoftwareVersion).filter_by(name=args.c[4]).first().id
	janaConfigId = session.query(JanaConfig).filter_by(name=args.c[5]).first().id
	janaCalibContextId = session.query(JanaCalibContext).filter_by(value=args.c[6]).first().id

	session.add(DataSet(args.c[0],dataTypeIndex,args.c[2],runPeriodIndex,softwareVersId,janaConfigId,janaCalibContextId))

# procedures for the -f (create DataSets from file) flag
if args.f is not None:
	pass

# runs the commit function here, as the modifications are done
session.commit()

#procedures for the -l,--list flag
if args.list:
	for i in range(1,session.query(DataSet).count()+1):
		print session.query(DataSet).filter_by(id=i).first()

session.close()
