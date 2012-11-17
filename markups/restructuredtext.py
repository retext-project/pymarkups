# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups.core import *
from markups.abstract import AbstractMarkup

class ReStructuredTextMarkup(AbstractMarkup):
	"""reStructuredText language"""
	name = 'reStructuredText'
	attributes = {
		LANGUAGE_HOME_PAGE: 'http://docutils.sourceforge.net/rst.html',
		MODULE_HOME_PAGE: 'http://docutils.sourceforge.net/',
		SYNTAX_DOCUMENTATION: 'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
	}
	
	file_extensions = ('.rst', '.rest')
	default_extension = '.rst'
	
	@staticmethod
	def available():
		try:
			import docutils.core
		except ImportError:
			return False
		return True
	
	def __init__(self, filename=None):
		AbstractMarkup.__init__(self, filename)
		from docutils.core import publish_parts
		self._publish_parts = publish_parts
	
	def publish_parts(self, text):
		if 'rest_parts' in self.cache:
			return self.cache['rest_parts']
		overrides = {'math_output': 'MathJax'}
		parts = self._publish_parts(text, writer_name='html',
			 settings_overrides=overrides)
		if self.enable_cache:
			self.cache['rest_parts'] = parts
		return parts
	
	def get_document_title(self, text):
		return self.publish_parts(text)['title']
	
	def get_document_body(self, text):
		return self.publish_parts(text)['body']
	
	def get_stylesheet(self, text=''):
		origstyle = self.publish_parts(text)['stylesheet']
		# Cut off <style> and </style> tags
		stylestart = '<style type="text/css">'
		stylesheet = ''
		if stylestart in origstyle:
			stylesheet = origstyle[origstyle.find(stylestart)+25:origstyle.rfind('</style>')]
		return stylesheet + get_pygments_stylesheet('.code')
	
	def get_javascript(self, text='', webenv=False):
		head = self.publish_parts(text)['head']
		start_position = head.find('<script ')
		end_position = head.rfind('</script>')
		if start_position >= 0 and end_position >= 0:
			mjurl = head[start_position:end_position+9]+'\n'
			return mjurl.replace(MATHJAX_WEB_URL, get_mathjax_url(webenv))
		return ''
