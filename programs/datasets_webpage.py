#!/usr/bin/env python

###################################################################################
# datasets_webpage.py - a simple cherrypy web application that generates 	  #
#			a webpage based on the DataSets table of the GlueX 	  #
#			Metadata DB.						  #
# Written by Joshua Freedman							  #
###################################################################################


import DatabaseConnection as DBC
import webpage_functions as WPF
import cherrypy
import consts
import sys
import os

db = None
try:
	db = DBC.DatabaseConnection(os.environ[consts.DB_ENV_VAR])
except DBC.InvalidDatabaseURLException as exc:
	print exc
	sys.exit(1)
except KeyError:
	print 'Set the environment variable \"{}\" to a valid database URL.'.format(consts.DB_ENV_VAR)
	sys.exit(1)

class Root:
	@cherrypy.expose
	def index(self,**kwargs):
		currentRP = None
		try:
			currentRP = db.search('RunPeriod','name',kwargs['dropdown'])[0]
		except KeyError:
			currentRP = db.list_all('RunPeriod')[0]

		RunPeriods = db.list_all('RunPeriod')
		
		attrs = [attr for attr in db.get_attributes('DataSet') if attr is not 'RunPeriod']
		dropdown = WPF.create_dropdown(RunPeriods,currentRP)
		tb_head = WPF.create_tableheadings(attrs)
		tb_data = ''
		for dataset in db.search('RunPeriod','name',currentRP.name)[0].DataSets:
			data = []
			for attr in attrs:
				data.append(getattr(dataset, attr))
			tb_data += WPF.create_tabledata(data)	
		style = '<style>th { padding-bottom: 5px; background-color: #aaaaaa;}td { padding-bottom: 5px; }</style>'
		return style + '<h2>GlueX DataSets</h2><b>Run Periods:</b>' + dropdown + '<hr />' + WPF.table_wrapper(tb_head + tb_data)	
if __name__ == '__main__':
	cherrypy.quickstart(Root(),'/')
