# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

# MathJax pattern code is based on work by Rob Mayoff
# https://github.com/mayoff/python-markdown-mathjax

import sys
from markups.core import *
from markups.abstract import AbstractMarkup

class MarkdownMarkup(AbstractMarkup):
	"""Markdown language"""
	name = 'Markdown'
	attributes = {
		LANGUAGE_HOME_PAGE: 'http://daringfireball.net/projects/markdown/',
		MODULE_HOME_PAGE: 'https://github.com/Waylan/Python-Markdown/',
		SYNTAX_DOCUMENTATION: 'http://daringfireball.net/projects/markdown/syntax'
	}
	
	file_extensions = ('.md', '.mkd', '.mkdn', '.mdwn', '.mdown', '.markdown')
	default_extension = '.mkd'
	
	@staticmethod
	def available():
		try:
			import markdown
		except:
			return False
		return True
	
	def _load_extensions_list_from_file(self, filename):
		try:
			extensions_file = open(filename)
		except IOError:
			return []
		else:
			extensions = [line.rstrip() for line in extensions_file]
			extensions_file.close()
			return extensions
	
	def _get_mathjax_pattern(self, markdown):
		def handleMatch(m):
			node = markdown.util.etree.Element('mathjax')
			node.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(2))
			return node
		pattern = markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$?)(.+?)\2')
		pattern.handleMatch = handleMatch
		return pattern
	
	def __init__(self, filename=None):
		import markdown
		self.extensions = self._load_extensions_list_from_file(
			CONFIGURATION_DIR + 'markdown-extensions.txt')
		local_directory = os.path.split(filename)[0] if filename else '.'
		if not local_directory: local_directory = '.'
		self.local_extensions = self._load_extensions_list_from_file(
			local_directory+'/markdown-extensions.txt')
		try:
			if not (self.extensions or self.local_extensions):
				self.extensions = ['extra']
			self.md = markdown.Markdown(self.extensions + self.local_extensions,
			output_format='html4')
		except (ValueError, ImportError) as e:
			sys.stderr.write(e)
			sys.stderr.write('\n')
			try:
				self.md = markdown.Markdown(self.extensions, output_format='html4')
			except (ValueError, ImportError) as e:
				sys.stderr.write(e)
				sys.stderr.write('\n')
				self.md = markdown.Markdown(output_format='html4')
		self.md.inlinePatterns.add('mathjax', self._get_mathjax_pattern(markdown),
		'<escape')
	
	def get_document_title(self, text):
		try:
			return str.join(' ', self.md.Meta['title'])
		except:
			return ''
	
	def get_stylesheet(self, text=''):
		if 'codehilite' in self.extensions + self.local_extensions:
			return get_pygments_stylesheet('.codehilite')
		return ''
	
	def get_javascript(self, text='', webenv=False):
		return ('<script type="text/javascript" src="' + get_mathjax_url(webenv)
		+ '?config=TeX-AMS-MML_HTMLorMML"></script>\n<script type="text/javascript">\n' +
		'MathJax.Hub.Config({ "tex2jax": { inlineMath: [[ \'$\', \'$\' ]] } });\n'
		+ '</script>\n')
	
	def get_document_body(self, text):
		self.md.reset()
		return self.md.convert(text)
