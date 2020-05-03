import os

class DirectoryConfiguration():
	def __init__(self):
		self._CUR_DIR = os.path.dirname(os.path.realpath(__file__))
		self._BASE_DIR = os.path.realpath(os.path.join(self._CUR_DIR, ".."))
		self._STATIC_DIR = os.path.realpath(os.path.join(self._CUR_DIR, "..", "static/"))
		self._PLOT_PICTURES_DIR = os.path.realpath(os.path.join(self._CUR_DIR, "..", "static", "images/"))
		self._CSV_DIR = os.path.realpath(os.path.join(self._CUR_DIR, "..", "csv/"))

	@property
	def CUR_DIR(self):
		return self._CUR_DIR
	
	@property
	def BASE_DIR(self):
		return self._BASE_DIR
	
	@property
	def STATIC_DIR(self):
		return self._STATIC_DIR
	
	@property
	def PLOT_PICTURES_DIR(self):
		return self._PLOT_PICTURES_DIR
	
	@property
	def CSV_DIR(self):
		return self._CSV_DIR
		
class UrlFilesConfiguration():
	def __init__(self):
		self._STATIC_URL = '/static'
		self._IMAGES_URL = '/static/images'

	@property
	def STATIC_URL(self):
		return self._STATIC_URL
	
	@property
	def IMAGES_URL(self):
		return self._IMAGES_URL


def series_to_table_html(series, name="", header=[]):
	index = list(series.index.array)
	values = list(series.values)

	# cria o header
	data = ('<h3>%s</h3><table style="border: 1px solid black;"><tr>' % name)
	for i in header:
		data += "<th>" + str(i) + "</th>"
	data += "</tr>"

	# insere os valores
	for i in range(len(index)):
		data += "<tr><td>" + str(index[i]) + "</td><td>"+ str(values[i]) + "</td></tr>"
	data += "</table><br />" 

	return data




	