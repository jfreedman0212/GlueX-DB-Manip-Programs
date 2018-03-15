#!/usr/bin/env python

###############################################################################
# DataSetManip.py - A command line program that manipulates the DataSet table #
#		    Written by Joshua Freedman				      #
#									      #
# Usages: ./DataSetManip.py <flags>					      #
#	-s <pathToDBFile>: Sets the env var to the specified path	      #
#	-c <NickName> <DataTypeName> <Revision>				      #
#		<RunPeriodName> <SoftwareVersionName>			      #
#		<JanaConfigName> <JanaCalibContextValue>: adds these values   #
#	-c <pathToFile>: adds all of the DataSets specified in the file      #
#			  in the same format as the -a command		      #
#	-

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
parser = argparse.ArgumentParser(description='Changes/Retrieves DataSets')
parser.add_argument()
#put arguments here
args = parser.parse_args()
