# GlueX Metadata Database Manipulation Programs
This repo contains some programs that manipulate the GlueX Metadata Database. They are: query.py, gluex_metadb_cmd.py, and datasets_webpage.py. They are located in the 
"programs" folder alongside other dependent files. The <a href="http://sqlalchemy.org">SQLAlchemy</a> library is used to communicate with the database. It also uses <a href="http://cherrypy.org">CherryPy</a> for the webpage program.
# Setup 
These programs use an environment variable that shows the path to the database file. So, if using bash for example, put this in your .bashrc or .bash_profile before using:
<code>export GLUEX_METADATA_DB="databaseURL"</code> The URL takes the form of: "sqlite:///[path to DB file]" or "mysql://[username]:[password]@[host]:[port]/[path]".
SQLite and MySQL are supported as of now. 
For more information on how the database URL works, refer to <a href="http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls">the SQLAlchemy documentation on database URLs</a>. Additionally, the PYTHONPATH variable
must be configured. To do so, put this line in your .bashrc or .bash_profile: <code>export PYTHONPATH="path/to/repo:$PYTHONPATH"</code>

If you want to change the name of the environment variable, change the name of DB_ENV_VAR in programs/consts.py to the desired name.

