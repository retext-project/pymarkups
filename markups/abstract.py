# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2018

whole_html_template = """<!doctype html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
{custom_headers}<title>{title}</title>
{stylesheet}{javascript}</head>
<body>
{body}
</body>
</html>
"""


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
		stylesheet = ('<style type="text/css">\n' + self.get_stylesheet()
			+ '</style>\n' if include_stylesheet else '')

		context = {
			"body": self.get_document_body(),
			"title": self.get_document_title() or fallback_title,
			"javascript": self.get_javascript(webenv),
			"stylesheet": stylesheet,
			"custom_headers": custom_headers,
		}
		return whole_html_template.format(**context)
