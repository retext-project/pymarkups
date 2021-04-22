# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2021

from __future__ import annotations

from typing import Any, Dict, Tuple, Optional

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


class AbstractMarkup:
	"""Abstract class for markup languages.

	:param filename: optional name of the file
	"""

	#: name of the markup visible to user
	name: str
	#: various attributes, like links to website and syntax documentation
	attributes: Dict[int, Any]
	#: indicates which file extensions are associated with the markup
	file_extensions: Tuple[str, ...]
	#: the default file extension
	default_extension: str

	def __init__(self, filename: Optional[str] = None):
		self.filename = filename

	@staticmethod
	def available() -> bool:
		"""
		:returns: whether the markup is ready for use

		          (for example, whether the required third-party
		          modules are importable)
		"""
		return True

	def convert(self, text: str) -> ConvertedMarkup:
		"""
		:returns: a ConvertedMarkup instance (or a subclass thereof)
		          containing the markup converted to HTML
		"""
		raise NotImplementedError


class ConvertedMarkup:
	"""This class encapsulates the title, body, stylesheet and javascript
	of a converted document.

	Instances of this class are created by :meth:`.AbstractMarkup.convert`
	method, usually it should not be instantiated directly.
	"""

	def __init__(self, body: str, title: str = '',
	             stylesheet: str = '', javascript: str = ''):
		self.title = title
		self.stylesheet = stylesheet
		self.javascript = javascript
		self.body = body

	def get_document_title(self) -> str:
		"""
		:returns: the document title
		"""
		return self.title

	def get_document_body(self) -> str:
		"""
		:returns: the contents of the ``<body>`` HTML tag
		"""
		return self.body

	def get_stylesheet(self) -> str:
		"""
		:returns: the contents of ``<style type="text/css">`` HTML tag
		"""
		return self.stylesheet

	def get_javascript(self, webenv: bool = False) -> str:
		"""
		:returns: one or more HTML tags to be inserted into the document
		          ``<head>``.
		:param webenv: if true, the specific markups may optimize the
		               document for being used in the World Wide Web (for
		               example, a remote version of MathJax script can be
		               inserted instead of the local one).
		"""
		return self.javascript

	def get_whole_html(self, custom_headers: str = '', include_stylesheet: bool = True,
	                   fallback_title: str = '', webenv: bool = False) -> str:
		"""
		:returns: the full contents of the HTML document (unless overridden
		          this is a combination of the previous methods)
		:param custom_headers: custom HTML to be inserted into the document
		                       ``<head>``
		:param include_stylesheet: if false, the stylesheet will not
		                           be included in the document ``<head>``
		:param fallback_title: when impossible to get the ``<title>`` from
		                       the document, this string can be used as a
		                       fallback
		:param webenv: like in :meth:`~.ConvertedMarkup.get_javascript`
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
