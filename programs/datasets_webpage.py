#!/usr/bin/env python

###################################################################################
# datasets_webpage.py - a simple cherrypy web application that generates 	  #
#			a webpage based on the DataSets table of the GlueX 	  #
#			Metadata DB.						  #
# Written by Joshua Freedman							  #
###################################################################################

from gluex_metadb_utils import databaseconnection as DBC
from gluex_metadb_utils import webpagefunctions as WPF
from gluex_metadb_utils import constants as consts
import cherrypy
import sys
import os

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
		try:
			currentRP = db.search('RunPeriod','name',kwargs['dropdown'])[0]
		except KeyError:
			if db.list_all('RunPeriod'):
				currentRP = db.list_all('RunPeriod')[0]
			else:
				return '<h2>GlueX DataSets</h2><p>The table is empty.</p>'	

		RunPeriods = db.list_all('RunPeriod')
		
		attrs = [attr for attr in db.get_attributes('DataSet') if attr != 'RunPeriod' and attr != 'revision' and attr != 'DataType']
		attrs.insert(0,'DataType')
		attrs.insert(1,'revision')
		dropdown = WPF.create_dropdown(RunPeriods,currentRP)
		tb_head = WPF.create_tableheadings(attrs)
		tb_data = ''
		for dataset in currentRP.DataSets:
			data = []
			for attr in attrs:
				data.append(getattr(dataset, attr))
			tb_data += WPF.create_tabledata(data)	
		style = """<style>
				th { padding-bottom: 5px; background-color: #aaaaaa;}
				td { padding-bottom: 5px; }
				.clickable {color:blue;}
				.clickable:hover {text-decoration: underline; cursor:pointer;}
			</style>"""
		return style + '<h2>GlueX DataSets</h2><b>Run Periods:</b>' + dropdown + '<hr />' + WPF.table_wrapper(tb_head + tb_data)	
if __name__ == '__main__':
	cherrypy.quickstart(Root(),'/')
