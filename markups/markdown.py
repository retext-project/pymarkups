# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2015

from __future__ import absolute_import

import importlib
import os
import re
import warnings
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

extensions_re = re.compile(r'required.extensions: ([ \w\.\(\),=_]+)', flags=re.IGNORECASE)

class MarkdownMarkup(AbstractMarkup):
	"""Markup class for Markdown language.
	Inherits :class:`~markups.abstract.AbstractMarkup`.

	:param extensions: list of extension names
	:type extensions: list
	"""
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
		lines = text.splitlines()
		match = extensions_re.search(lines[0]) if lines else None
		if match:
			return match.group(1).strip().split()
		return []

	def _canonicalize_extension_name(self, extension_name):
		lb = extension_name.find('(')
		if lb >= 0:
			extension_name, parameters = extension_name[:lb], extension_name[lb:]
		else:
			parameters = ''
		prefixes = ('markdown.extensions.', '', 'mdx_')
		for prefix in prefixes:
			try:
				module = importlib.import_module(prefix + extension_name)
				if not hasattr(module, 'makeExtension'):
					continue
			except (ImportError, ValueError, TypeError):
				pass
			else:
				return prefix + extension_name + parameters

	def _apply_extensions(self):
		extensions = (self.requested_extensions or
			self.global_extensions) + self.document_extensions
		extensions_final = []
		should_push_extra = True
		should_push_mathjax = (True, False)
		for extension in extensions:
			if extension == 'mathjax':
				should_push_mathjax = (True, True)
			elif extension == 'remove_extra':
				should_push_extra = False
				should_push_mathjax = (False, )
			else:
				canonical_name = self._canonicalize_extension_name(extension)
				if not canonical_name:
					warnings.warn('Extension "%s" does not exist.' %
						extension, ImportWarning)
					continue
				if canonical_name not in extensions_final:
					extensions_final.append(canonical_name)
		if should_push_extra:
			extensions_final.append('markdown.extensions.extra')
		if should_push_mathjax[0]:
			extensions_final.append('markups.mdx_mathjax(enable_dollar_delimiter=%r)' %
				should_push_mathjax[1])
		self.md = self.markdown.Markdown(extensions=extensions_final, output_format='html4')
		self.extensions = extensions_final

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
		if 'markdown.extensions.meta' not in self.extensions:
			return ''
		if hasattr(self.md, 'Meta') and 'title' in self.md.Meta:
			return str.join(' ', self.md.Meta['title'])
		else:
			return ''

	def get_stylesheet(self, text=''):
		if 'markdown.extensions.codehilite' in self.extensions:
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
