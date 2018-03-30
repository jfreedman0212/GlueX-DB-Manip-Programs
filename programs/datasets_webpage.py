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
		outputString += '<tr><th>id</th><th>nickname</th><th>dataType</th><th>revision</th>'
		outputString += '<th>runPeriod</th><th>softwareVersion</th><th>janaConfig</th>'
		outputString += '<th>janaCalibContext</th></tr>'
		for i in range(1,session.query(DataSet).count()+1):
			current = session.query(DataSet).filter_by(id=i).first()
			outputString += '<tr>'
			outputString += '<td>{}</td><td>{}</td>'.format(current.id,current.nickname)
			outputString += '<td>{}</td>'.format(session.query(DataType).filter_by(id=current.dataTypeId).first().name)
			outputString += '<td>{}</td>'.format(current.revision)
			outputString += '<td>{}</td>'.format(session.query(RunPeriod).filter_by(id=current.runPeriodId).first().name)
			outputString += '<td>{}</td>'.format(session.query(SoftwareVersion).filter_by(id=current.softwareVersionId).first().name)
			outputString += '<td>{}</td>'.format(session.query(JanaConfig).filter_by(id=current.janaConfigId).first().name)
			outputString += '<td>{}</td>'.format(session.query(JanaCalibContext).filter_by(id=current.janaCalibContextId).first().value)
			outputString += '</tr>'
		outputString += '</table></body></html>'
		return outputString
if __name__ == '__main__':
	cherrypy.quickstart(Root(),'/')
