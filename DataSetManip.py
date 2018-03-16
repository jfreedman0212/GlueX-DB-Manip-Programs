#!/usr/bin/env python

###############################################################################
# DataSetManip.py - A command line program that manipulates the DataSet table #
#		    that also updates a webpage every time a new DataSet is   #
#		    created.						      #
# Written by Joshua Freedman						      #
###############################################################################

# import dependencies
import os
import consts # has the name for the env variable to the database file
import argparse
from pydoc import locate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gluex_metadata_classes import * 

# sqlalchemy setup
engine = create_engine('sqlite:///{}'.format(os.environ[consts.DB_ENV_VAR])) 
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# argparse setup
parser = argparse.ArgumentParser(description='Creates/Lists DataSets')
parser.add_argument('-s',metavar='pathToDB',help='changes the environment variable for the DB file to the specified pathname')
parser.add_argument('-c',metavar=('nickName','dataType','revision','runPeriod','softwareVersion','janaConfig','janaCalibContext'),\
		    nargs=7,help='creates a new DataSet with the specified values for each attribute of it')
parser.add_argument('-f',metavar='pathToFile',help='creates several DataSets from the specified file (file should be in format of -c flag)')
parser.add_argument('-l','--list',action='store_true',help='lists all of the DataSets in a user-friendly format')
args = parser.parse_args()

# runs the modification procedures first, then the display procedure 
# if a modification and a display flag are both called

# procedures for the -s (set env var) flag
if args.s is not None:
	pass

# procedures for the -c (create DataSet) flag
if args.c is not None:
	pass

# procedures for the -f (create DataSets from file) flag
if args.f is not None:
	pass

# runs the commit function here, as the modifications are done
session.commit()

#procedures for the -l,--list flag
if args.list:
	pass

session.close()
