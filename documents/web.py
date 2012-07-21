# python-documents, web module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import os
import documents
from email.utils import formatdate

__version__ = documents.__version__
site = 'https://launchpad.net/python-documents'

APP_NAME, APP_VERSION, APP_SITE = range(3)
default_app_data = ('python-documents', __version__, site)

class WebLibrary(object):
	def __init__(self, working_dir='.', app_data=default_app_data):
		"""Construct a new WebLibrary object"""
		self.working_dir = working_dir
		if app_data[APP_SITE]:
			self.app_info = '<a href="' + app_data[APP_SITE] + '">' \
			+ app_data[APP_NAME] + '</a>'
		else:
			self.app_info = app_data[APP_NAME]
		if app_data[APP_VERSION]:
			self.generator_info = app_data[APP_NAME] + ' ' + app_data[APP_VERSION]
		else:
			self.generator_info = app_data[APP_VERSION]
	
	def update_all(self):
		"""Process all documents in the directory"""
		self._init_template()
		for fname in filter(os.path.isfile, os.listdir(self.working_dir)):
			self._process_page(fname)
	
	def update(self, filename):
		"""Process one file in the directory"""
		self._init_template()
		if os.path.exists(self.working_dir+'/'+filename):
			self._process_page(filename)
	
	def _init_template(self):
		templatefile = open(self.working_dir+'/template.html')
		try:
			self.template = unicode(templatefile.read(), 'utf-8')
		except:
			# For Python 3
			self.template = templatefile.read()
		templatefile.close()
		self.template = self.template.replace('%GENERATOR%', self.generator_info)
		self.template = self.template.replace('%APPINFO%', self.app_info)
	
	def _process_page(self, fname):
		bn, ext = os.path.splitext(fname)
		html = pagename = ''
		inputfile = open(self.working_dir+'/'+fname, 'r')
		try:
			text = unicode(inputfile.read(), 'utf-8')
		except:
			# For Python 3
			text = inputfile.read()
		inputfile.close()
		markup = documents.get_markup_for_file_name(fname)
		if not markup:
			return
		html = markup.get_document_body(text)
		pagename = markup.get_document_title(text)
		javascript = markup.get_javascript(text)
		if not pagename:
			pagename = bn
		if html or bn == 'index':
			content = self.template
			content = content.replace('%CONTENT%', html)
			try:
				pagename = unicode(pagename, 'utf-8')
				bn = unicode(bn, 'utf-8')
			except:
				pass # Not needed for Python 3
			content = content.replace('%PAGENAME%', pagename)
			content = content.replace('%EXTRAHEADERS%', javascript)
			content = content.replace('%HTMLDIR%', '.')
			content = content.replace('%MARKUPNAME%', markup.name)
			content = content.replace('%TIME%', formatdate(usegmt=True))
			content = content.replace(' href="'+bn+'.html"', '')
			content = content.replace('%\\', '%')
			outputfile = open(self.working_dir+'/html/'+bn+'.html', 'w')
			try:
				outputfile.write(content.encode('utf-8'))
			except:
				# For Python 3
				outputfile.write(content)
			outputfile.close()
