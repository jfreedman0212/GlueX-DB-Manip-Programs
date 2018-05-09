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

	# dialect: a string referring to the type of DB system being used (currently supports mysql and sqlite)
	# dialect defaults to sqlite if invalid
	# pathToDB: a string that holds the path to the DB file, can be either relative or absolute
	def __init__(self,dialect,pathToDB=None):
		# verifies the dialect is valid
		# can add more supported dialects here if necessary
		if dialect is not 'mysql':
			dialect = 'sqlite'

		dburl = '{}://'.format(dialect)
		if pathToDB is not None:
			if dialect is 'sqlite':
				pathToDB = '/' + pathToDB
		else:
			# gives a default name in the current directory
			pathToDB = 'gluex_metadata_db'

		# engine setup
		self._engine = create_engine(dburl)
		Base.metadata.create_all(self._engine)
		
		# session setup
		Base.metadata.bind = self._engine
		self._session_creator = sessionmaker(bind=self._engine)
		self._session = self._session_creator()

	# takes a variable number of parameters (depending on 
	def create(self,table,*args,**kwargs):
		pass
	
	def remove(self,table,index):
		dataToBeRemoved = self.search(table,'id',index)
		self._session.delete(dataToBeRemoved[0])

	def changeDatabaseFile(self,newFile):
		pass

	def search(self,table,attr,key):
		filterQuery = self._session.query(locate('gluex_metadata_classes.'+table)).filter(locate('gluex_metadata_classes.'+table).name is key)
		return filterQuery.all()
	
"""
	# should i even have a destructor? is there another way to do this?
	def __del__(self):
		self._session.close()
"""
