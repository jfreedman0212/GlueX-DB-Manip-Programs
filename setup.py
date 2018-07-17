from setuptools import setup

with open('README.md', 'r') as f:
	long_desc = f.read()

setup(
	name='gluex_metadb_programs',
	description='Some programs that utilize the GlueX metadata database',
	long_description = long_desc,
	long_description_content_type='text/markdown',
	author='Joshua Freedman',
	author_email='jfreedman0212@gmail.com',
	url='https://github.com/jfreedman0212/GlueX-DB-Manip-Programs',
	scripts=[
		'programs/query.py',
		'programs/datasets_webpage.py',
		'programs/gluex_metadb_cmd.py'
	],
	install_requires=[
		'sqlalchemy',
		'alembic',
		'cherrypy'
	],
	classifiers=(
		'Programming Language :: Python :: 2.7',
	)
)
