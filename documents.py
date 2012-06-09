# python-documents
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import os.path

(NAME, LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(4)

CONFIGURATION_DIR = os.path.expanduser('~/.config/python-documents/')

class AbstractMarkup(object):
	"""Abstract class for markup languages"""
	
	file_extensions = ()
	
	def __init__(filename=None):
		raise NotImplementedError()
		
	def available():
		raise NotImplementedError()
	
	def get_document_title(self, text):
		raise NotImplementedError()
	
	def get_document_body(self, text):
		raise NotImplementedError()

class MarkdownMarkup(AbstractMarkup):
	"""Markdown language"""
	attributes = {
		NAME: 'Markdown',
		LANGUAGE_HOME_PAGE: 'http://daringfireball.net/projects/markdown/',
		MODULE_HOME_PAGE: 'https://github.com/Waylan/Python-Markdown/',
		SYNTAX_DOCUMENTATION: 'http://daringfireball.net/projects/markdown/syntax'
	}
	
	file_extensions = ('.md', '.mkd', '.mkdn', '.mdwn', '.mdown', '.markdown')
	
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
	
	def __init__(self, filename=None):
		import markdown
		self.extensions = self._load_extensions_list_from_file(
			CONFIGURATION_DIR + 'markdown-extensions.txt')
		local_directory = os.path.split(filename)[0] if filename else '.'
		self.local_extensions = self._load_extensions_list_from_file(
			local_directory+'/markdown-extensions.txt')
		try:
			self.md = markdown.Markdown(self.extensions + self.local_extensions,
			output_format='html4')
		except ValueError as e:
			try:
				self.md = markdown.Markdown(self.extensions, output_format='html4')
			except ValueError:
				self.md = markdown.Markdown(output_format='html4')
	
	def get_document_title(self, text):
		try:
			return str.join(' ', self.md.Meta['title'])
		except:
			return ''
	
	def get_document_body(self, text):
		self.md.reset()
		return self.md.convert(text)

class ReStructuredTextMarkup(AbstractMarkup):
	"""reStructuredText language"""
	attributes = {
		NAME: 'reStructuredText',
		LANGUAGE_HOME_PAGE: 'http://docutils.sourceforge.net/rst.html',
		MODULE_HOME_PAGE: 'http://docutils.sourceforge.net/',
		SYNTAX_DOCUMENTATION: 'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
	}
	
	file_extensions = ('.rst', '.rest')
	
	def available():
		try:
			from docutils.core import publish_parts
		except:
			return False
		return True
	
	def __init__(self, filename=None):
		from docutils.core import publish_parts
		self.publish_parts = publish_parts
	
	def get_document_title(self, text):
		return self.publish_parts(text, writer_name='html')['title']
	
	def get_document_body(self, text):
		return self.publish_parts(text, writer_name='html')['body']

available_markups = (MarkdownMarkup, ReStructuredTextMarkup)

def get_markup_for_file_name(filename):
	markup_class = None
	for markup in available_markups:
		for extension in markup.file_extensions:
			if filename.endswith(extension):
				markup_class = markup
	if markup_class:
		return markup_class(filename=filename)
