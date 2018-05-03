# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2018

import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup


class ReStructuredTextMarkup(AbstractMarkup):
	"""Markup class for reStructuredText language.
	Inherits :class:`~markups.abstract.AbstractMarkup`.

	:param settings_overrides: optional dictionary of overrides for the
	                           `Docutils settings`_
	:type settings_overrides: dict

	.. _`Docutils settings`: http://docutils.sourceforge.net/docs/user/config.html
	"""
	name = 'reStructuredText'
	attributes = {
		common.LANGUAGE_HOME_PAGE: 'http://docutils.sourceforge.net/rst.html',
		common.MODULE_HOME_PAGE: 'http://docutils.sourceforge.net/',
		common.SYNTAX_DOCUMENTATION: 'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
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

	def __init__(self, filename=None, settings_overrides=None):
		self.overrides = settings_overrides or {}
		self.overrides.update({
			'math_output': 'MathJax %s?config=TeX-AMS_CHTML' % common.MATHJAX_WEB_URL,
			'syntax_highlight': 'short',
		})
		AbstractMarkup.__init__(self, filename)
		from docutils.core import publish_parts
		self._publish_parts = publish_parts

	def convert(self, text):
		parts = self._publish_parts(text, source_path=self.filename,
			writer_name='html5', settings_overrides=self.overrides)

		# Determine head
		head = parts['head']

		# Determine body
		body = parts['html_body']

		# Determine title
		title = parts['title']

		# Determine stylesheet
		origstyle = parts['stylesheet']
		# Cut off <style> and </style> tags
		stylestart = '<style type="text/css">'
		stylesheet = ''
		if stylestart in origstyle:
			stylesheet = origstyle[origstyle.find(stylestart)+25:origstyle.rfind('</style>')]
		stylesheet += common.get_pygments_stylesheet('.code')

		return ConvertedReStructuredText(head, body, title, stylesheet)


class ConvertedReStructuredText(ConvertedMarkup):

	def __init__(self, head, body, title, stylesheet):
		ConvertedMarkup.__init__(self, body, title, stylesheet)
		self.head = head

	def get_javascript(self, webenv=False):
		if 'MathJax.js?config=TeX-AMS_CHTML' not in self.head:
			return ''
		return ('<script type="text/javascript" src="%s?config=TeX-AMS_CHTML"></script>\n' %
		        common.get_mathjax_url(webenv))
