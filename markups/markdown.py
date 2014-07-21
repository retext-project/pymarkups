# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from __future__ import absolute_import

import os
import re
import sys
import markups.common as common
from markups.abstract import AbstractMarkup

MATHJAX_CONFIG = \
'''<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"],
  TeX: {
    equationNumbers: {autoNumber: "AMS"}
  }
});
</script>
'''

extensions_re = re.compile(r'required.extensions: ([ \w]+)', flags=re.IGNORECASE)

class MarkdownMarkup(AbstractMarkup):
	"""Markdown language"""
	name = 'Markdown'
	attributes = {
		common.LANGUAGE_HOME_PAGE: 'http://daringfireball.net/projects/markdown/',
		common.MODULE_HOME_PAGE: 'https://github.com/Waylan/Python-Markdown/',
		common.SYNTAX_DOCUMENTATION: 'http://daringfireball.net/projects/markdown/syntax'
	}

	file_extensions = ('.md', '.mkd', '.mkdn', '.mdwn', '.mdown', '.markdown')
	default_extension = '.mkd'

	@staticmethod
	def available():
		try:
			import markdown
		except ImportError:
			return False
		return True

	def _load_extensions_list_from_file(self, filename):
		try:
			extensions_file = open(filename)
		except IOError:
			return []
		else:
			extensions = [line.rstrip() for line in extensions_file
			              if not line.startswith('#')]
			extensions_file.close()
			return extensions

	def _get_global_extensions(self, filename):
		extensions = self._load_extensions_list_from_file(
			os.path.join(common.CONFIGURATION_DIR, 'markdown-extensions.txt'))
		local_directory = os.path.dirname(filename) if filename else ''
		extensions += self._load_extensions_list_from_file(
			os.path.join(local_directory, 'markdown-extensions.txt'))
		return extensions

	def _get_document_extensions(self, text):
		firstline = text.splitlines()[0]
		match = extensions_re.search(firstline)
		if match:
			return match.group(1).strip().split()
		return []

	def _check_extension_exists(self, extension_name):
		try:
			__import__('markdown.extensions.'+extension_name, {}, {},
			['markdown.extensions'])
		except ImportError:
			try:
				__import__('mdx_'+extension_name)
			except ImportError:
				return False
		return True

	def _get_mathjax_patterns(self):
		def handle_match_inline(m):
			node = self.markdown.util.etree.Element('script')
			node.set('type', 'math/tex')
			node.text = self.markdown.util.AtomicString(m.group(3))
			return node

		def handle_match(m):
			node = self.markdown.util.etree.Element('script')
			node.set('type', 'math/tex; mode=display')
			node.text = self.markdown.util.AtomicString(m.group(3))
			if '\\begin' in m.group(2):
				node.text = self.markdown.util.AtomicString(m.group(2) +
				m.group(3) + m.group(4))
			return node

		inlinemathpatterns = (
			self.markdown.inlinepatterns.Pattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),  #  $...$
			self.markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\()(.+?)(\\\))')     # \(...\)
		)
		mathpatterns = (
			self.markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'), # $$...$$
			self.markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),    # \[...\]
			self.markdown.inlinepatterns.Pattern(r'(?<!\\)(\\begin{[a-z]+\*?})(.+)(\\end{[a-z]+\*?})')
		)
		if not self.mathjax:
			inlinemathpatterns = inlinemathpatterns[1:]
		patterns = []
		for pattern in inlinemathpatterns:
			pattern.handleMatch = handle_match_inline
			patterns.append(pattern)
		for pattern in mathpatterns:
			pattern.handleMatch = handle_match
			patterns.append(pattern)
		return patterns

	def _apply_extensions(self):
		extensions = (self.requested_extensions or
			self.global_extensions) + self.document_extensions
		# Remove duplicate entries
		extensions = list(set(extensions))
		# We have two "virtual" extensions
		self.mathjax = ('mathjax' in extensions)
		self.remove_mathjax = ('remove_extra' in extensions)
		if 'remove_extra' in extensions:
			extensions.remove('remove_extra')
		elif 'extra' not in extensions:
			extensions.append('extra')
		if self.mathjax:
			extensions.remove('mathjax')
		for extension in extensions:
			if not extension:
				extensions.remove(extension)
				continue
			if not self._check_extension_exists(extension):
				sys.stderr.write('Extension "%s" does not exist.\n' % extension)
				extensions.remove(extension)
		self.md = self.markdown.Markdown(extensions, output_format='html4')
		for i, pattern in enumerate(self._get_mathjax_patterns()):
			self.md.inlinePatterns.add('mathjax%d' % i, pattern, '<escape')
		self.extensions = extensions

	def __init__(self, filename=None, extensions=None):
		AbstractMarkup.__init__(self, filename)
		import markdown
		self.markdown = markdown
		self.requested_extensions = extensions or []
		self.global_extensions = self._get_global_extensions(filename)
		self.document_extensions = []
		self._apply_extensions()

	def get_document_title(self, text):
		if not 'body' in self._cache:
			self.get_document_body(text)
		if 'meta' not in self.extensions:
			return ''
		if hasattr(self.md, 'Meta') and 'title' in self.md.Meta:
			return str.join(' ', self.md.Meta['title'])
		else:
			return ''

	def get_stylesheet(self, text=''):
		if 'codehilite' in self.extensions:
			return common.get_pygments_stylesheet('.codehilite')
		return ''

	def get_javascript(self, text='', webenv=False):
		if 'body' in self._cache:
			body = self._cache['body']
		else:
			body = self.get_document_body(text)
		if not '<script type="math/tex' in body:
			return ''
		return (MATHJAX_CONFIG + '<script type="text/javascript" src="'
		+ common.get_mathjax_url(webenv) + '"></script>')

	def get_document_body(self, text):
		self.md.reset()
		document_extensions = self._get_document_extensions(text)
		if document_extensions or self.document_extensions:
			self.document_extensions = document_extensions
			self._apply_extensions()
		converted_text = self.md.convert(text) + '\n'
		if self._enable_cache:
			self._cache['body'] = converted_text
		return converted_text
