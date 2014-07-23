# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2014

class AbstractMarkup(object):
	"""Abstract class for markup languages.

	:param filename: optional name of the file
	:type filename: str
	"""

	#: name of the markup visible to user
	name = ''
	#: various attributes, like links to website and syntax documentation
	attributes = {}
	#: indicates which file extensions are associated with the markup
	file_extensions = ()
	#: the default file extension
	default_extension = ''

	def __init__(self, filename=None):
		self.filename = filename
		self._enable_cache = False
		self._cache = {}

	@staticmethod
	def available():
		"""
		:returns: whether the markup is ready for use

		          (for example, whether the required third-party
		          modules are importable)
		:rtype: bool
		"""
		return True

	def get_document_title(self, text):
		"""
		:returns: the document title
		:rtype: str
		"""
		return ''

	def get_document_body(self, text):
		"""
		:returns: the contents of the ``<body>`` HTML tag
		:rtype: str
		"""
		raise NotImplementedError

	def get_stylesheet(self, text=''):
		"""
		:returns: the contents of ``<style type="text/css">`` HTML tag
		:rtype: str
		"""
		return ''

	def get_javascript(self, text='', webenv=False):
		"""
		:returns: one or more HTML tags to be inserted into the document
		          ``<head>``.
		:rtype: str
		"""
		return ''

	def get_whole_html(self, text, custom_headers='', include_stylesheet=True,
	                   fallback_title='', webenv=False):
		"""
		:returns: the full contents of the HTML document (unless overridden
		          this is a combination of the previous methods)
		:rtype: str
		"""
		self._enable_cache = True
		body = self.get_document_body(text)
		stylesheet = ('<style type="text/css">\n' + self.get_stylesheet(text)
			+ '</style>\n' if include_stylesheet else '')
		title = self.get_document_title(text)
		if not title:
			title = fallback_title
		title_string = ('<title>' + title + '</title>\n') if title else ''
		javascript = self.get_javascript(text, webenv)
		self._enable_cache = False
		self._cache = {}
		return (
		'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
		'<html>\n<head>\n'
		'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n'
		+ custom_headers + title_string + stylesheet + javascript
		+ '</head>\n<body>\n' + body + '</body>\n</html>\n'
		)
