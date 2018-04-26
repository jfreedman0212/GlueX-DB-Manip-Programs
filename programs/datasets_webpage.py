#!/usr/bin/env python

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
		outputString = '<html><head><title>GlueX DataSets</title>'
		outputString +='<style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style>'
		outputString += '</head><body><table>'
		first = session.query(DataSet).first()
		items = [a for a in dir(first) if not a.startswith('_') and not 'Id' in a and not callable(getattr(first,a))]
	
		outputString += '<tr>' 
		outputString += '<th>id</th>'
		outputString += '<th>nickname</th>'
		outputString += '<th>revision</th>'
		for item in items:
			if hasattr(getattr(first,item),'metadata'):
				outputString += '<th>{}</th>'.format(getattr(first,item).__class__.__name__)
		outputString += '</tr>'		

		for dataset in session.query(DataSet).all():
			outputString += '<tr>'
			outputString += '<td>{}</td>'.format(dataset.id)
			outputString += '<td>{}</td>'.format(dataset.nickname)
			outputString += '<td>{}</td>'.format(dataset.revision)
			for item in items:
				if hasattr(getattr(dataset,item),'metadata'):
					if hasattr(getattr(dataset,item),'name'):
						outputString += '<td>{}</td>'.format(getattr(dataset,item).name)
					else:
						outputString += '<td>{}</td>'.format(getattr(dataset,item).value)		
			outputString += '</tr>'
		outputString += '</table></body></html>'
		return outputString
if __name__ == '__main__':
	cherrypy.quickstart(Root(),'/')
