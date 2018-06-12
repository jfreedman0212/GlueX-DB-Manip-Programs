###############################################################################
# DatabaseConnection.py - A wrapper class for a SQLAlchemy session so that    #
#			  the user does not have to refer directly to the     #
#			  session object.				      #
# Written by Joshua Freedman						      #
###############################################################################

import gluex_metadata_classes as gluex_md
from pydoc import locate
import consts
import os
import re

# exception for the constructor to throw
class InvalidDatabaseURLException(Exception):
	pass

class DatabaseConnection:
	### private member data ###

	_session_creator = None
	_session = None
	_engine = None

	### public member functions ###

	# constructor
	# dburl: the database url, contains information about the dialect
	#	 and the path. sqlite and mysql support
	def __init__(self,dburl):
		# checks the dialect of dburl and does specific checking for each 
		# checks to see if they follow the pattern for the dialect
		if dburl.startswith('mysql'):
			pattern = 'mysql://.+(?:).*@.+(?:).*/.+'
			if re.match(pattern,dburl) is None:
				error_message = '\"{}\" is in an invalid form. '.format(dburl)
				error_message += 'Should follow this format: \n'
				error_message += 'mysql://[username]:[password]@[host]:[port]/[file]'
				raise InvalidDatabaseURLException(error_message)
		elif dburl.startswith('sqlite'):
			pattern = 'sqlite:///.*'
			if re.match(pattern,dburl) is None:
				error_message = '\"{}\" is in an invalid form. '.format(dburl)
				error_message += 'Should follow this format: \n'
				error_message += 'sqlite:///[pathToDatabaseFile].db'
				raise InvalidDatabaseURLException(error_message)
		else:
			raise InvalidDatabaseURLException('\"{}\" is invalid. Dialects mysql and sqlite supported.'.format(dburl))
		# engine setup
		self._engine = gluex_md.create_engine(dburl,connect_args={'check_same_thread':False})
		gluex_md.Base.metadata.create_all(self._engine)
		# session setup
		gluex_md.Base.metadata.bind = self._engine
		self._session_creator = gluex_md.sessionmaker(bind=self._engine)
		self._session = self._session_creator()
	
	# creates an entry in the database for the specified table
	# table: the table that is being acted upon
	# dictOfAttrs: dictionary of attributes that has a key-value pair
	#	       that corresponds to specific table
	def create(self,table,dictOfAttrs):
		newItem = locate('gluex_metadata_classes.'+table)()
		for key,value in dictOfAttrs.iteritems():
			if getattr(newItem,key,None) is not None:
				setattr(newItem,key,value)
			else:
				raise AttributeError('{} does not have attribute {}.'.format(table,key))
		self._session.add(newItem)
		self._session.commit()

	# updates an existing field's attribute to a new value
	# table: the table that is being acted upon
	# index: the index of the table being updated
	# attr: the attribute of the table entry to be changed
	# newValue: the new value of the attribute	
	def update(self,table,index,attr,newValue):
		tableref = locate('gluex_metadata_classes.' + table)
		updatedEntry = self._session.query(tableref).filter(tableref.id == index).first()
		if getattr(updatedEntry,attr,None) is not None:
			setattr(updatedEntry,attr,newValue)
		else:
			raise AttributeError('{} does not have attribute {}'.format(table,attr))
		self._session.commit()

	# deletes the specified row of the specified table
	# table: the table being acted upon
	# index: the id of the row being deleted
	def remove(self,table,index):
		tableref = locate('gluex_metadata_classes.' + table)
		self._session.query(tableref).filter(tableref.id == index).delete()
		self._session.commit()
	
	# returns all of the elements in a table with the specified value for the specified attribute
	# table: the table that is being acted upon
	# attr: the attribute that is trying to be matched
	# key: the desired value for that specific attribute
	def search(self,table,attr,key):
		tableref = locate('gluex_metadata_classes.'+table)
		if getattr(tableref(),attr,None) is None:
			raise AttributeError('{} does not have attribute {}'.format(table,attr))
		filterQuery = self._session.query(tableref).filter(getattr(tableref,attr) == key)
		return filterQuery.all()

	# returns an array of all of the entries in a table
	# table: the table being acted upon
	def list_all(self,table):
		tableref = locate('gluex_metadata_classes.' + table)
		return self._session.query(tableref).all()
	
	# returns an array of all the attributes for the specified table
	# these attributes are the ones that should be modified (such as 'name'
	# or 'comment', not the 'id' or other SQLAlchemy relationships).
	# table: the table being acted upon
	def get_attributes(self,table):
		tableref = locate('gluex_metadata_classes.' + table)
		attributes = [attr for attr in dir(tableref()) \
			      if not attr.startswith('_') \
			      and attr is not 'id' and 'Id' not in attr \
			      and not callable(getattr(tableref(), attr)) \
			      and 'DataSets' not in attr \
			      and attr is not 'metadata' and 'Id' not in attr]
		return attributes
	
	# returns an array of the tables in the database
	def get_tables(self):
		tables = [item for item in dir(gluex_md) if not item.startswith('_') \
			  and 'DeclarativeMeta' in type(getattr(gluex_md,item)).__name__ \
			  and item is not 'Base']
		return tables		

	# destructor to close the session whenever the object gets deleted
	def __del__(self):
		# checks b/c the __del__ still runs if the constructor raises an error
		if self._session is not None:
			self._session.close()
