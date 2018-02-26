#!/usr/bin/env python

# put big comment block here with description and usage of the program

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
#parser = argparse.ArgumentParser(description='Changes/Retrieves DataSets')
#parser.add_argument()
#put arguments here
#args = parser.parse_args()
