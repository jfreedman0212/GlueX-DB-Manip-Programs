###############################################################################
# DatabaseConnection.py - a wrapper class for a SQLAlchemy session so that    #
#			  the user does not have to refer directly to the     #
#			  session object.				      #
# Written by Joshua Freedman						      #
###############################################################################

from gluex_metadata_classes import *
from pydoc import locate

class DatabaseConnection:
	### private member data ###
	_session_creator = None
	_session = None
	_engine = None

	### public member functions ###

	# constructor
	# dialect: a string referring to the type of DB 
	#	   system being used (currently supports mysql and sqlite)
	# 	   dialect defaults to sqlite if invalid
	# pathToDB: a string that holds the path to the DB file
	#	    can be either relative or absolute
	def __init__(self,dialect,pathToDB=None):
		# verifies the dialect is valid
		# can add more supported dialects here if necessary
		if dialect is not 'mysql':
			dialect = 'sqlite'

		dburl = '{}://'.format(dialect)
		if pathToDB is None:
			# gives a default name in the current directory
			pathToDB = 'gluex_metadata_db.db'
		if dialect is 'sqlite':
			pathToDB = '/' + pathToDB

		dburl += pathToDB

		# engine setup
		self._engine = create_engine(dburl)
		Base.metadata.create_all(self._engine)
		
		# session setup
		Base.metadata.bind = self._engine
		self._session_creator = sessionmaker(bind=self._engine)
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
				raise AttributeError('Table {} does not have attribute {}.'.format(table,key))
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
			raise AttributeError('Table {} does not have attribute {}'.format(table,attr))
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
		filterQuery = self._session.query(tableref).filter(getattr(tableref,attr) == key)
		return filterQuery.all()
	
	# destructor to close the session whenever the object gets deleted
	def __del__(self):
		self._session.close()

