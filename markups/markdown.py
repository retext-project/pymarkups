# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2018

import importlib
import os
import re
import warnings
import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup

try:
	import yaml
except ImportError:
	yaml = None

MATHJAX2_CONFIG = \
'''<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "input/AsciiMath", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"],
  TeX: {
    extensions: ["AMSmath.js", "AMSsymbols.js"],
    equationNumbers: {autoNumber: "AMS"}
  }
});
</script>
'''

# Taken from:
# https://docs.mathjax.org/en/latest/upgrading/v2.html?highlight=upgrading#changes-in-the-mathjax-api
MATHJAX3_CONFIG = \
'''
<script>
MathJax = {
  options: {
    renderActions: {
      find: [10, function (doc) {
        for (const node of document.querySelectorAll('script[type^="math/tex"]')) {
          const display = !!node.type.match(/; *mode=display/);
          const math = new doc.options.MathItem(node.textContent, doc.inputJax[0], display);
          const text = document.createTextNode('');
          node.parentNode.replaceChild(text, node);
          math.start = {node: text, delim: '', n: 0};
          math.end = {node: text, delim: '', n: 0};
          doc.math.push(math);
        }
      }, '']
    }
  }
};
</script>
'''

extensions_re = re.compile(r'required.extensions: (.+)', flags=re.IGNORECASE)
extension_name_re = re.compile(r'[a-z0-9_.]+(?:\([^)]+\))?', flags=re.IGNORECASE)

_canonicalized_ext_names = {}

class MarkdownMarkup(AbstractMarkup):
	"""Markup class for Markdown language.
	Inherits :class:`~markups.abstract.AbstractMarkup`.

	:param extensions: list of extension names
	:type extensions: list
	"""
	name = 'Markdown'
	attributes = {
		common.LANGUAGE_HOME_PAGE: 'https://daringfireball.net/projects/markdown/',
		common.MODULE_HOME_PAGE: 'https://github.com/Python-Markdown/markdown',
		common.SYNTAX_DOCUMENTATION: 'https://daringfireball.net/projects/markdown/syntax'
	}

	file_extensions = ('.md', '.mkd', '.mkdn', '.mdwn', '.mdown', '.markdown')
	default_extension = '.mkd'

	@staticmethod
	def available():
		try:
			import markdown
		except ImportError:
			return False
		return (hasattr(markdown, '__version_info__') or  # underscored attribute means 3.x
		        hasattr(markdown, 'version_info') and markdown.version_info >= (2, 6))

	def _load_extensions_list_from_txt_file(self, filename):
		with open(filename) as extensions_file:
			for line in extensions_file:
				if not line.startswith('#'):
					yield self._split_extension_config(line.rstrip())

	def _load_extensions_list_from_yaml_file(self, filename):
		with open(filename) as extensions_file:
			try:
				data = yaml.safe_load(extensions_file)
			except yaml.YAMLError as ex:
				warnings.warn(f'Failed parsing {filename}: {ex}', SyntaxWarning)
				raise IOError from ex
		if isinstance(data, list):
			for item in data:
				if isinstance(item, dict):
					yield from item.items()
				elif isinstance(item, str):
					yield item, {}

	def _get_global_extensions(self, filename):
		local_directory = os.path.dirname(filename) if filename else ''
		choices = [
			os.path.join(local_directory, 'markdown-extensions.yaml'),
			os.path.join(local_directory, 'markdown-extensions.txt'),
			os.path.join(common.CONFIGURATION_DIR, 'markdown-extensions.yaml'),
			os.path.join(common.CONFIGURATION_DIR, 'markdown-extensions.txt'),
		]
		for choice in choices:
			try:
				if choice.endswith('.txt'):
					yield from self._load_extensions_list_from_txt_file(choice)
				elif choice.endswith('.yaml') and yaml:
					yield from self._load_extensions_list_from_yaml_file(choice)
			except IOError:
				continue  # Cannot open file, move to the next choice
			else:
				break  # File loaded successfully, skip the remaining choices

	def _get_document_extensions(self, text):
		lines = text.splitlines()
		match = extensions_re.search(lines[0]) if lines else None
		if match:
			extensions = extension_name_re.findall(match.group(1))
			yield from self._split_extensions_configs(extensions)

	def _canonicalize_extension_name(self, extension_name):
		prefixes = ('markdown.extensions.', '', 'mdx_')
		for prefix in prefixes:
			try:
				module = importlib.import_module(prefix + extension_name)
				if not hasattr(module, 'makeExtension'):
					continue
			except (ImportError, ValueError, TypeError):
				pass
			else:
				return prefix + extension_name

	def _split_extension_config(self, extension_name):
		"""Splits the configuration options from the extension name."""
		lb = extension_name.find('(')
		if lb == -1:
			return extension_name, {}
		extension_name, parameters = extension_name[:lb], extension_name[lb + 1:-1]
		pairs = [x.split("=") for x in parameters.split(",")]
		return extension_name, {x.strip(): y.strip() for (x, y) in pairs}

	def _split_extensions_configs(self, extensions):
		"""Splits the configuration options from a list of strings.

		:returns: a generator of (name, config) tuples
		"""
		for extension in extensions:
			yield self._split_extension_config(extension)

	def _apply_extensions(self, document_extensions=None):
		extensions = self.global_extensions
		extensions.extend(
			self._split_extensions_configs(self.requested_extensions))
		if document_extensions is not None:
			extensions.extend(document_extensions)

		extension_names = {"markdown.extensions.extra", "mdx_math"}
		extension_configs = {}

		for name, config in extensions:
			if name == 'mathjax':
				mathjax_config = {"enable_dollar_delimiter": True}
				extension_configs["mdx_math"] = mathjax_config
			elif name == 'remove_extra':
				if "markdown.extensions.extra" in extension_names:
					extension_names.remove("markdown.extensions.extra")
				if "mdx_math" in extension_names:
					extension_names.remove("mdx_math")
			else:
				if name in _canonicalized_ext_names:
					canonical_name = _canonicalized_ext_names[name]
				else:
					canonical_name = self._canonicalize_extension_name(name)
					if canonical_name is None:
						warnings.warn('Extension "%s" does not exist.' %
							name, ImportWarning)
						continue
					_canonicalized_ext_names[name] = canonical_name
				extension_names.add(canonical_name)
				extension_configs[canonical_name] = config
		self.md = self.markdown.Markdown(extensions=list(extension_names),
		                                 extension_configs=extension_configs,
		                                 output_format='html5')
		self.extensions = extension_names
		self.extension_configs = extension_configs

	def __init__(self, filename=None, extensions=None):
		AbstractMarkup.__init__(self, filename)
		import markdown
		self.markdown = markdown
		self.requested_extensions = extensions or []
		self.global_extensions = []
		if extensions is None:
			self.global_extensions.extend(self._get_global_extensions(filename))
		self._apply_extensions()

	def convert(self, text):

		# Determine body
		self.md.reset()
		self._apply_extensions(self._get_document_extensions(text))
		body = self.md.convert(text) + '\n'

		# Determine title
		if hasattr(self.md, 'Meta') and 'title' in self.md.Meta:
			title = str.join(' ', self.md.Meta['title'])
		else:
			title = ''

		# Determine stylesheet
		css_class = None

		if 'markdown.extensions.codehilite' in self.extensions:
			config = self.extension_configs.get('markdown.extensions.codehilite', {})
			css_class = config.get('css_class', 'codehilite')
			stylesheet = common.get_pygments_stylesheet('.%s' % css_class)
		elif 'pymdownx.highlight' in self.extensions:
			config = self.extension_configs.get('pymdownx.highlight', {})
			css_class = config.get('css_class', 'highlight')
			stylesheet = common.get_pygments_stylesheet('.%s' % css_class)
		else:
			stylesheet = ''

		return ConvertedMarkdown(body, title, stylesheet)

class ConvertedMarkdown(ConvertedMarkup):

	def get_javascript(self, webenv=False):
		if '<script type="math/' not in self.body:
			return ''
		mathjax_url, mathjax_version = common.get_mathjax_url_and_version(webenv)
		config = MATHJAX3_CONFIG if mathjax_version == 3 else MATHJAX2_CONFIG
		async_attr = ' async' if mathjax_version == 3 else ''
		script_tag = '<script type="text/javascript" src="%s"%s></script>'
		return config + script_tag % (mathjax_url, async_attr)
