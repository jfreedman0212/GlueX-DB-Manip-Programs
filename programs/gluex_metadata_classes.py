# these classes define the data for the gluex database
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
	def __init__(self,nname='No Name',dtid=1,rev='ver00',rpid=1,sftwrverid=1,jcid=1,jccid=1):
		self.nickname = nname
		self.dataTypeId = dtid
		self.revision = rev
		self.runPeriodId = rpid
		self.softwareVersionId = sftwrverid
		self.janaConfigId = jcid
		self.janaCalibContextId = jccid

	def getString(self,session):
		outputString = 'id:{}'.format(self.id)
		outputString += 'nickname: {}'.format(self.nickname)
#		outputString += ''.format(


#engine setup
engine = create_engine('sqlite:///{}'.format(os.environ[consts.DB_ENV_VAR]))
Base.metadata.create_all(engine)

# session setup
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
