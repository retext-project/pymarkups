# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2014

from functools import wraps
from warnings import warn

def _deprecated(function_in):
	@wraps(function_in)
	def function_out(*args, **kwargs):
		warn('Method %s() is deprecated. Please use convert() instead.' %
		     function_in.__name__, DeprecationWarning, stacklevel=2)
		return function_in(*args, **kwargs)
	return function_out

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

	@staticmethod
	def available():
		"""
		:returns: whether the markup is ready for use

		          (for example, whether the required third-party
		          modules are importable)
		:rtype: bool
		"""
		return True

	def convert(self, text):
		"""
		:returns: a ConvertedMarkup instance (or a subclass thereof)
		          containing the markup converted to HTML
		:rtype: ConvertedMarkup
		"""
		raise NotImplementedError

	@_deprecated
	def get_document_title(self, text):
		return self.convert(text).get_document_title()

	@_deprecated
	def get_document_body(self, text):
		return self.convert(text).get_document_body()

	@_deprecated
	def get_stylesheet(self, text=''):
		return self.convert(text).get_stylesheet()

	@_deprecated
	def get_javascript(self, text='', **kwargs):
		return self.convert(text).get_javascript(**kwargs)

	@_deprecated
	def get_whole_html(self, text, **kwargs):
		return self.convert(text).get_whole_html(**kwargs)


class ConvertedMarkup(object):
	"""This class encapsulates the title, body, stylesheet and javascript
	of a converted document.

	Instances of this class are created by :meth:`.AbstractMarkup.convert`
	method, usually it should not be instantiated directly.
	"""

	def __init__(self, body, title='', stylesheet='', javascript=''):
		self.title = title
		self.stylesheet = stylesheet
		self.javascript = javascript
		self.body = body

	def get_document_title(self):
		"""
		:returns: the document title
		:rtype: str
		"""
		return self.title

	def get_document_body(self):
		"""
		:returns: the contents of the ``<body>`` HTML tag
		:rtype: str
		"""
		return self.body

	def get_stylesheet(self):
		"""
		:returns: the contents of ``<style type="text/css">`` HTML tag
		:rtype: str
		"""
		return self.stylesheet

	def get_javascript(self, webenv=False):
		"""
		:returns: one or more HTML tags to be inserted into the document
		          ``<head>``.
		:rtype: str
		:param bool webenv: if true, the specific markups may optimize the
		                    document for being used in the World Wide Web (for
		                    example, a remote version of MathJax script can be
		                    inserted instead of the local one).
		"""
		return self.javascript

	def get_whole_html(self, custom_headers='', include_stylesheet=True,
	                   fallback_title='', webenv=False):
		"""
		:returns: the full contents of the HTML document (unless overridden
		          this is a combination of the previous methods)
		:rtype: str
		:param str custom_headers: custom HTML to be inserted into the document
		                           ``<head>``
		:param bool include_stylesheet: if false, the stylesheet will not
		                                be included in the document ``<head>``
		:param str fallback_title: when impossible to get the ``<title>`` from
		                           the document, this string can be used as a
		                           fallback
		:param bool webenv: like in :meth:`~.ConvertedMarkup.get_javascript`
		                    above
		"""
		body = self.get_document_body()
		stylesheet = ('<style type="text/css">\n' + self.get_stylesheet()
			+ '</style>\n' if include_stylesheet else '')
		title = self.get_document_title()
		if not title:
			title = fallback_title
		title_string = ('<title>' + title + '</title>\n') if title else ''
		javascript = self.get_javascript(webenv)
		return (
		'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
		'<html>\n<head>\n'
		'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n'
		+ custom_headers + title_string + stylesheet + javascript
		+ '</head>\n<body>\n' + body + '</body>\n</html>\n'
		)
