# these classes define the data for the gluex database
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# these are the sqlalchemy classes for the gluex database as laid out in the schema
class DataType(Base):
	__tablename__ = 'DataType'
	id = Column(Integer, primary_key=True)
	name = Column(String(250)) 
	comment = Column(String(250))
	def __str__(self):
		return str(self.id)+'|'+self.name+'|'+self.comment
	def __init__(self):
		super(DataType,self).__init__()
		self.name = 'none'
		self.comment = 'none'
class RunPeriod(Base):
	__tablename__ = 'RunPeriod'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	def __str__(self):
		return str(self.id)+'|'+self.name+'|'+self.comment
	def __init__(self):
		super(RunPeriod,self).__init__()
		self.name = 'none'
		self.comment = 'none'
class SoftwareVersion(Base):
	__tablename__ = 'SoftwareVersion'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	def __str__(self):
		return str(self.id)+'|'+self.name+'|'+self.comment
	def __init__(self):
		super(SoftwareVersion,self).__init__()
		self.name = 'none'
		self.comment = 'none'
class JanaConfig(Base):
	__tablename__ = 'JanaConfig'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	comment = Column(String(250))
	content = Column(String(250))
	def __str__(self):
		return str(self.id)+'|'+self.name+'|'+self.comment+'|'+self.content
	def __init__(self):
		super(JanaConfig,self).__init__()
		self.name = 'none'
		self.comment = 'none'
		self.content= 'none'
class JanaCalibContext(Base):
	__tablename__ = 'JanaCalibContext'
	id = Column(Integer, primary_key = True)
	value = Column(String(250))
	def __str__(self):
		return str(self.id)+'|'+self.value
	def __init__(self):
		super(JanaCalibContext,self).__init__()
		self.name = 'none'
		self.value = 'none'
# this class should be right? i might need to add relationships to these (one to one i believe)
# also determine how to format the __str__() function
class DataSet(Base):
	__tablename__ = 'DataSet'
	id = Column(Integer, primary_key = True)
	nickname = Column(String(250))
	dataTypeId = Column(Integer, ForeignKey("DataType.id"))
	revision = Column(String(250))
	runPeriodId = Column(Integer, ForeignKey("RunPeriod.id"))
	softwareVersionId = Column(Integer, ForeignKey("SoftwareVersion.id"))
	janaConfigId = Column(Integer, ForeignKey("JanaConfig.id"))
	janaCalibContextId = Column(Integer, ForeignKey("JanaCalibContext.id"))
	versionStringTag = Column(String(250))
	#def __str(self):
	#	pass
engine = create_engine('sqlite:///gluex_metadata.db')
 
Base.metadata.create_all(engine)
