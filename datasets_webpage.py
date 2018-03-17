###################################################################################
# datasets_webpage.py: a simple cherrypy web application that generates a webpage #
#		       based on the DataSets table of the GlueX Metadata DB.      #
# Written by Joshua Freedman							  #
###################################################################################

# import dependencies
import cherrypy
from gluex_metadata_classes import *

class Root:
	@cherrypy.expose
	def index(self):
		outputString = ''
		for i in range(1,session.query(DataType).count()+1):
			outputString = outputString + str(session.query(DataType).filter_by(id=i).first()) + '\n'
		return outputString
if __name__ == '__main__':
	cherrypy.quickstart(Root(),'/')
