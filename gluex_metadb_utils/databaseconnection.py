###############################################################################
# databaseconnection.py - A wrapper class for a SQLAlchemy session so that    #
#			  the user does not have to refer directly to the     #
#			  session object.				      #
# Written by Joshua Freedman						      #
###############################################################################

import metadatamodel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import os
import re

# exception for the constructor to throw
class InvalidDatabaseURLException(Exception):
	pass

# exception raised if an invalid table is given
class TableError(Exception):
	pass

# a "special none" for special cases where there is no
# actual value for a specific attribute (couldnt use NoneType
# because that was a possible value for some values)
class SpecialNone(object):
	pass

spn = SpecialNone()

class DatabaseConnection(object):
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
		self._engine = create_engine(dburl,connect_args={'check_same_thread':False})
		metadatamodel.Base.metadata.create_all(self._engine)
		# session setup
		metadatamodel.Base.metadata.bind = self._engine
		self._session_creator = sessionmaker(bind=self._engine)
		self._session = self._session_creator()
	
	# creates an entry in the database for the specified table
	# can raise an IOError if the content field is not given an existing file
	# can also raise an AttributeError if the attribute specified does not exist
	# table: the table that is being acted upon
	# dictOfAttrs: dictionary of attributes that has a key-value pair
	#	       that corresponds to specific table
	def create(self,table,dictOfAttrs):
		self.check_table(table)
		newItem = getattr(metadatamodel, table)()
		for key,value in dictOfAttrs.iteritems():
			if getattr(newItem,key,spn) is not spn:
				# checks for content because this field will be entered as
				# a file name, and should be checked for here
				if key == 'content':
					value = open(value,'r').read()
				setattr(newItem,key,value)
			else:
				raise AttributeError('\"{}\" does not have attribute \"{}\".'.format(table,key))
		self._session.add(newItem)
		self._session.commit()

	# updates an existing field's attribute to a new value,
	# can throw IndexError if an invalid index is given or
	# an AttributeError if an invalid attribute is given
	# table: the table that is being acted upon
	# index: the index of the table being updated
	# attr: the attribute of the table entry to be changed
	# newValue: the new value of the attribute	
	def update(self,table,index,attr,newValue):
		self.check_table(table)
		tableref = getattr(metadatamodel, table)
		updatedEntry = None
		try:
			updatedEntry = self._session.query(tableref).filter(tableref.id == index).one()
		except NoResultFound:
			raise IndexError('The index \"{}\" does not exist for table \"{}\".'.format(index,table))

		if getattr(updatedEntry,attr,spn) is not spn:
			# checks for content because this field will be entered as
			# a file name, and should be checked for here
			if attr == 'content':
				newValue = open(newValue,'r').read()
			setattr(updatedEntry,attr,newValue)
		else:
			raise AttributeError('\"{}\" does not have attribute \"{}\"'.format(table,attr))
		self._session.commit()

	# deletes the specified row of the specified table
	# can throw IndexError if an invalid index is given
	# table: the table being acted upon
	# index: the id of the row being deleted
	def remove(self,table,index):
		self.check_table(table)
		tableref = getattr(metadatamodel, table)
		deletedEntry = self._session.query(tableref).filter(tableref.id == index)

		try:
			deletedEntry.one()
		except NoResultFound:
			raise IndexError('The index \"{}\" does not exist for table \"{}\".'.format(index,table))

		deletedEntry.delete()
		self._session.commit()
	
	# returns all of the elements in a table with the specified value for the specified attribute
	# table: the table that is being acted upon
	# attr: the attribute that is trying to be matched
	# key: the desired value for that specific attribute
	def search(self,table,attr,key):
		self.check_table(table)
		tableref = getattr(metadatamodel, table)
		if getattr(tableref(),attr,spn) is spn:
			raise AttributeError('\"{}\" does not have attribute \"{}\"'.format(table,attr))
		filterQuery = self._session.query(tableref).filter(getattr(tableref,attr) == key)
		return filterQuery.all()

	# returns an array of all of the entries in a table
	# table: the table being acted upon
	def list_all(self,table):
		self.check_table(table)
		tableref = getattr(metadatamodel ,table)
		return self._session.query(tableref).all()

	# destructor to close the session whenever the object gets deleted
	def __del__(self):
		# checks b/c the __del__ still runs if the constructor raises an error
		if self._session is not None:
			self._session.close()

	### static/class methods ###

	# if the table is invalid, raises a TableError exception
	# table: the table being checked
	@classmethod
	def check_table(cls,table):
		if table not in cls.get_tables():
			error_message = '\"{}\" is not a valid table. The valid tables are:'.format(table)
			for table in cls.get_tables():
				error_message += '\n' + table
			raise TableError(error_message)

	# returns an array of all the attributes for the specified table
	# these attributes are the ones that should be modified (such as 'name'
	# or 'comment', not the 'id' or other SQLAlchemy relationships).
	# table: the table being acted upon
	@staticmethod
	def get_attributes(table):
		DatabaseConnection.check_table(table)
		attributes = [attr.name.split('.',1)[0] for attr in metadatamodel.Base.metadata.tables[table].columns]
		for attr in attributes:
			if attr.endswith('Id'):
				index = attributes.index(attr)
				attributes[index] = attributes[index][:-2]
		return attributes
	
	# returns an array of the tables in the database
	@staticmethod
	def get_tables():
		return [table.name for table in metadatamodel.Base.metadata.sorted_tables]
