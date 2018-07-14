###################################################################################
# webpagefunctions.py - some functions used in generating a webpage, intended     #
#			 for the datasets_webpage.py program			  # 
# Written by Joshua Freedman							  #
###################################################################################

### dropdown creation functions ###
def select_wrapper(creator_func):
	def wrapper(item,selected):
		return """<form method="POST" onchange="document.forms[0].submit()" action="/">
				<select name="dropdown">{}</select>
			  </form>""".format(creator_func(item,selected))
	return wrapper

# creates an html dropdown using the values given by the array
@select_wrapper
def create_dropdown(array,selected):
	out = ''
	for item in array:
		add = ''
		if item is selected:
			add = 'selected'
		out += '<option value="{0}" name=\"{0}\" {1}>{0}</option>'.format(str(item),add)
	return out

### table creation functions ###

# wraps a string with the opening and closing table tags
def table_wrapper(string):
	return '<table>' + string + '</table>'

# to be used as a decorator for the following table functions
def tablerow_wrapper(creator_func):
	def wrapper(item):
		return '<tr>{}</tr>'.format(creator_func(item))
	return wrapper

# creates a row of table headings
@tablerow_wrapper
def create_tableheadings(array):
	out = ''
	for item in array:
		out += '<th>{}</th>'.format(str(item))
	return out

# creates a row of table data
@tablerow_wrapper
def create_tabledata(array):
	out = ''
	for item in array:
		extraAttr = ''
		try:
			extraAttr = 'class="clickable" onclick="alert({})"'.format(str(item.content).__repr__())
		except AttributeError:
			pass
		out += '<td {1}>{0}</td>'.format(str(item),extraAttr)
	return out

