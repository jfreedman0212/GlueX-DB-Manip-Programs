###############################################################################
# gluex_metadata_classes.py - The SQLAlchemy classes that describe the        #
#			      GlueX Metadata Database based on the schema.    #
# Written by Joshua Freedman						      #
###############################################################################

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

### these are the sqlalchemy classes for the metadata DB ###

class DataType(Base):
	__tablename__ = 'DataType'
	id = Column(Integer, primary_key=True)
	name = Column(String(250)) 
	comment = Column(String(250))
	DataSets = relationship('DataSet',back_populates='DataType')

	def __str__(self):
		return self.name

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
		return self.name

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
		return self.name

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
		return self.name

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
		return self.value

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

	DataTypeId = Column(Integer,ForeignKey('DataType.id'))
	DataType = relationship('DataType',back_populates='DataSets')

	RunPeriodId = Column(Integer,ForeignKey('RunPeriod.id'))
	RunPeriod = relationship('RunPeriod',back_populates='DataSets')

	SoftwareVersionId = Column(Integer,ForeignKey('SoftwareVersion.id'))
	SoftwareVersion = relationship('SoftwareVersion',back_populates='DataSets')
	
	JanaConfigId = Column(Integer,ForeignKey('JanaConfig.id'))
	JanaConfig = relationship('JanaConfig',back_populates='DataSets')
	
	JanaCalibContextId = Column(Integer,ForeignKey('JanaCalibContext.id'))
	JanaCalibContext = relationship('JanaCalibContext',back_populates='DataSets')

	# class methods
	def __init__(self,nname='No Name',dtid=0,rev='No Version Specified',rpid=0,sftwrverid=0,jcid=0,jccid=0):
		super(DataSet,self).__init__()
		self.nickname = nname
		self.DataTypeId = dtid
		self.revision = rev
		self.RunPeriodId = rpid
		self.SoftwareVersionId = sftwrverid
		self.JanaConfigId = jcid
		self.JanaCalibContextId = jccid

	def __str__(self):
		output = '{}|{}|{}|{}|{}|{}|{}'.format(self.nickname,self.revision,self.DataType, \
					               self.RunPeriod, self.SoftwareVersion, self.JanaConfig, \
					               self.JanaCalibContext)
		return output

	def data_version_string(self):
		return '{}_{}_{}'.format(self.DataType,self.RunPeriod,self.revision)
