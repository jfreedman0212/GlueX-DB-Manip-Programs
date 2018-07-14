from setuptools import setup

setup(
	scripts=[
		'programs/query.py',
		'programs/datasets_webpage.py',
		'programs/gluex_metadb_cmd.py'
	],
	install_requires=[
		'sqlalchemy',
		'alembic',
		'cherrypy'
	]
)
