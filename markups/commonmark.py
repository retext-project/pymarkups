# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: BSD
# Copyright: (C) Shengjing Zhu, 2016

import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup

try:
	from CommonMark import HtmlRenderer, Parser
	from CommonMark.common import escape_xml
except:
	pass


class CommonMarkMarkup(AbstractMarkup):
	"""Markup class for CommonMark language.
	Inherits :class:`~markups.abstract.AbstractMarkup`.
	"""
	name = 'CommonMark'
	attributes = {
		common.LANGUAGE_HOME_PAGE: 'http://commonmark.org/',
		common.MODULE_HOME_PAGE: 'https://github.com/rtfd/CommonMark-py/',
		common.SYNTAX_DOCUMENTATION: 'http://spec.commonmark.org/'
	}

	# Note: the same as MarkdownMarkup
	# file_extensions = ('.md', '.mkd', '.mkdn', '.mdwn', '.mdown', '.markdown')
	# default_extension = '.md'

	@staticmethod
	def available():
		try:
			import CommonMark
		except ImportError:
			return False
		return True

	def __init__(self, filename=None, options={}):
		self.enable_highlight = options.get('highlight', True)
		super().__init__(filename)
		self.parse = Parser().parse
		if self.enable_highlight:
			self.render = CommonMarkRender(options).render
		else:
			self.render = HtmlRenderer(options).render

	def convert(self, text):
		ast = self.parse(text)
		html = self.render(ast)
		if self.enable_highlight:
			stylesheet = common.get_pygments_stylesheet('.highlight')
		else:
			stylesheet = ''
		return ConvertedMarkup(html, stylesheet=stylesheet)


class CommonMarkRender(HtmlRenderer):
	def __init__(self, options):
		super().__init__(options)

	def code_block(self, node, entering):
		try:
			from pygments import highlight, lexers, formatters
		except ImportError:
			return super().code_block(node, entering)
		info_words = node.info.split() if node.info else []
		language = ''
		if len(info_words) > 0 and len(info_words[0]) > 0:
			language = escape_xml(info_words[0], True)
		try:
			lexer = lexers.get_lexer_by_name(language)
		except:
			return super().code_block(node, entering)
		attrs = self.attrs(node)
		attrs.append(['class', 'highlight language-' + language])
		code = node.literal
		result = highlight(code, lexer, formatters.HtmlFormatter(nowrap=True))
		self.cr()
		self.tag('pre')
		self.tag('code', attrs)
		self.lit(result)
		self.tag('/code')
		self.tag('/pre')
		self.cr()
