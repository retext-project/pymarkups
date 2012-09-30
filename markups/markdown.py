# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from __future__ import absolute_import

import sys
from markups.core import *
from markups.abstract import AbstractMarkup

MATHJAX_CONFIG = '''
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [ ["$", "$"], ["\\\\(", "\\\\)"] ],
    processEscapes: true
  }
});
</script>
'''

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
	
	def _get_mathjax_patterns(self, markdown):
		def handle_match_inline(m):
			node = markdown.util.etree.Element('span')
			node.set('class', 'math')
			node.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(4))
			return node
		
		def handle_match(m):
			node = markdown.util.etree.Element('div')
			node.set('class', 'math')
			node.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(4))
			return node
		
		inlinemathpatterns = (
			markdown.inlinepatterns.Pattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),
			markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\()([^\\)]+)(\\\))')
		)
		mathpatterns = (
			markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'),
			markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\[)(.+)(\\\])'),
			markdown.inlinepatterns.Pattern(r'(?<!\\)(\\begin{[a-z]+\*?})(.+)(\\end{[a-z]+\*?})')
		)
		patterns = []
		for pattern in inlinemathpatterns:
			pattern.handleMatch = handle_match_inline
			patterns.append(pattern)
		for pattern in mathpatterns:
			pattern.handleMatch = handle_match
			patterns.append(pattern)
		return patterns
	
	def __init__(self, filename=None):
		AbstractMarkup.__init__(self, filename)
		import markdown
		self.extensions = self._load_extensions_list_from_file(
			CONFIGURATION_DIR + 'markdown-extensions.txt')
		local_directory = os.path.split(filename)[0] if filename else '.'
		if not local_directory: local_directory = '.'
		self.extensions += self._load_extensions_list_from_file(
			local_directory+'/markdown-extensions.txt')
		# Remove duplicate entries
		self.extensions = list(set(self.extensions))
		# We have two virtual extensions
		if 'remove_extra' in self.extensions:
			self.extensions.remove('remove_extra')
		else:
			self.extensions.append('extra')
		self.mathjax = ('mathjax' in self.extensions)
		if self.mathjax:
			self.extensions.remove('mathjax')
		for extension in self.extensions:
			if not self._check_extension_exists(extension):
				sys.stderr.write('Failed loading extension %s\n' % extension)
				self.extensions.remove(extension)
		self.md = markdown.Markdown(self.extensions, output_format='html4')
		if self.mathjax:
			patterns = self._get_mathjax_patterns(markdown)
			for i in range(len(patterns)):
				self.md.inlinePatterns.add('mathjax%d' % i, patterns[i], '<escape')
	
	def get_document_title(self, text):
		if 'meta' not in self.extensions:
			return ''
		if not 'body' in self.cache:
			self.get_document_body(text)
		return str.join(' ', self.md.Meta['title'])
	
	def get_stylesheet(self, text=''):
		if 'codehilite' in self.extensions:
			return get_pygments_stylesheet('.codehilite')
		return ''
	
	def get_javascript(self, text='', webenv=False):
		if not self.mathjax:
			return ''
		if 'body' in self.cache:
			body = self.cache['body']
		else:
			body = self.get_document_body(text)
		if not 'class="math"' in body:
			return ''
		return ('<script type="text/javascript" src="' + get_mathjax_url(webenv)
		+ '?config=TeX-AMS-MML_HTMLorMML"></script>' + MATHJAX_CONFIG)
	
	def get_document_body(self, text):
		self.md.reset()
		converted_text = self.md.convert(text) + '\n'
		if self.enable_cache:
			self.cache['body'] = converted_text
		return converted_text
