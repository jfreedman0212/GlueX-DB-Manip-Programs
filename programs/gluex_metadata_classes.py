###############################################################################
# gluex_metadata_classes.py - the SQLAlchemy classes that describe the        #
#			      GlueX Metadata Database. Also contains a class  #
#			      that allows easy interaction with the Database. #
# Written by Joshua Freedman						      #
###############################################################################

import os
import sys
import consts
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

# these are the sqlalchemy classes for the gluex database as laid out in the schema
class DataType(Base):
	__tablename__ = 'DataType'
	id = Column(Integer, primary_key=True)
	name = Column(String(250)) 
	comment = Column(String(250))
	# DataSets attribute holds all of the DataSets that have a specific instance of DataType as
	# its DataType
	DataSets = relationship('DataSet',back_populates='DataType')
	def __str__(self):
		return 'id: {}\nname: {}\ncomment: {}'.format(self.id,self.name,self.comment)
	def __init__(self,n='none',c='none'):
		super(DataType,self).__init__()
		self.name = n
		self.comment = c
class RunPeriod(Base):
	__tablename__ = 'RunPeriod'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	DataSets = relationship('DataSet',back_populates='RunPeriod')
	def __str__(self):
		return 'id: {}\nname: {}\ncomment: {}'.format(self.id,self.name,self.comment)
	def __init__(self,n='none',c='none'):
		super(RunPeriod,self).__init__()
		self.name = n
		self.comment = c
class SoftwareVersion(Base):
	__tablename__ = 'SoftwareVersion'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	DataSets = relationship('DataSet',back_populates='SoftwareVersion')
	def __str__(self):
		return 'id: {}\nname: {}\ncomment: {}'.format(self.id,self.name,self.comment)
	def __init__(self,n='none',c='none'):
		super(SoftwareVersion,self).__init__()
		self.name = n
		self.comment = c
class JanaConfig(Base):
	__tablename__ = 'JanaConfig'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	content = Column(String(250))
	DataSets = relationship('DataSet',back_populates='JanaConfig')
	def __str__(self):
		return 'id: {}\nname: {}\ncomment: {}\ncontent: {}'.format(self.id,self.name,self.comment,self.content)
	def __init__(self,n='none',c='none',ct='none'):
		super(JanaConfig,self).__init__()
		self.name = n
		self.comment = c
		self.content= ct
class JanaCalibContext(Base):
	__tablename__ = 'JanaCalibContext'
	id = Column(Integer, primary_key = True)
	value = Column(String(250))
	DataSets = relationship('DataSet',back_populates='JanaCalibContext')
	def __str__(self):
		return 'id: {}\nvalue: {}'.format(self.id,self.value)
	def __init__(self,v='none'):
		super(JanaCalibContext,self).__init__()
		self.value = v
class DataSet(Base):
	__tablename__ = 'DataSet'
	id = Column(Integer, primary_key=True)
	nickname = Column(String(250))
	revision = Column(String(250))

	# the remaining class members represent the DataSet table's relationships with the other tables
	# if you want to add another table that DataSet relates to, create the class like the ones above
	# and create a relationship between the two like the ones below

	dataTypeId = Column(Integer,ForeignKey('DataType.id'))
	DataType = relationship('DataType',back_populates='DataSets')

	runPeriodId = Column(Integer,ForeignKey('RunPeriod.id'))
	RunPeriod = relationship('RunPeriod',back_populates='DataSets')

	softwareVersionId = Column(Integer,ForeignKey('SoftwareVersion.id'))
	SoftwareVersion = relationship('SoftwareVersion',back_populates='DataSets')
	
	janaConfigId = Column(Integer,ForeignKey('JanaConfig.id'))
	JanaConfig = relationship('JanaConfig',back_populates='DataSets')
	
	janaCalibContextId = Column(Integer,ForeignKey('JanaCalibContext.id'))
	JanaCalibContext = relationship('JanaCalibContext',back_populates='DataSets')

	# class methods
	def __init__(self,nname='No Name',dtid=0,rev='No Version Specified',rpid=0,sftwrverid=0,jcid=0,jccid=0):
		super(DataSet,self).__init__()
		self.nickname = nname
		self.dataTypeId = dtid
		self.DataType = None
		self.revision = rev
		self.runPeriodId = rpid
		self.RunPeriod = None
		self.softwareVersionId = sftwrverid
		self.SoftwareVersion = None
		self.janaConfigId = jcid
		self.JanaConfig = None
		self.janaCalibContextId = jccid
		self.JanaCalibContext = None

	def __str__(self):
		output = '{}|{}|{}|{}|{}|{}|{}|{}'.format(self.id,self.nickname,self.revision,self.DataType.name, \
						   	  self.RunPeriod.name, self.SoftwareVersion.name, self.JanaConfig.name, \
							  self.JanaCalibContext.value)
		return output

### TO BE DELETED ###
#engine setup
engine = create_engine('sqlite:///{}'.format(os.environ[consts.DB_ENV_VAR]))
Base.metadata.create_all(engine)

# session setup
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
