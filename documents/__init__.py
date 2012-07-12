# python-documents
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

__version__ = '0.2'

import os.path

(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)

CONFIGURATION_DIR = os.path.expanduser('~/.config/python-documents/')

class AbstractMarkup(object):
	"""Abstract class for markup languages"""
	
	file_extensions = ()
	
	def __init__(self, filename=None):
		raise NotImplementedError()
	
	def available():
		raise NotImplementedError()
	
	def get_document_title(self, text):
		raise NotImplementedError()
	
	def get_document_body(self, text):
		raise NotImplementedError()
	
	def get_stylesheet(self, text=''):
		return ''
	
	def get_javascript(self, text=''):
		return ''
	
	def get_whole_html(self, text, custom_headers='',
	                   include_stylesheet=True, fallback_title=''):
		stylesheet = ('<style type="text/css">\n' + self.get_stylesheet(text) +
			'</style>\n' if include_stylesheet else '')
		title = self.get_document_title(text)
		if not title:
			title = fallback_title
		title_string = ('<title>' + title + '</title>\n') if title else ''
		return (
		'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
		'<html>\n<head>\n'
		'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n'
		+ custom_headers + title_string + stylesheet + self.get_javascript(text)
		+ '</head>\n<body>\n' + self.get_document_body(text)
		+ '</body>\n</html>\n'
		)

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
	
	def get_stylesheet(self, text=''):
		if 'codehilite' in self.extensions + self.local_extensions:
			try:
				from pygments.formatters import HtmlFormatter
			except:
				pass
			else:
				return HtmlFormatter().get_style_defs('.codehilite') + '\n'
		return ''
	
	def get_document_body(self, text):
		self.md.reset()
		return self.md.convert(text)

class ReStructuredTextMarkup(AbstractMarkup):
	"""reStructuredText language"""
	name = 'reStructuredText'
	attributes = {
		LANGUAGE_HOME_PAGE: 'http://docutils.sourceforge.net/rst.html',
		MODULE_HOME_PAGE: 'http://docutils.sourceforge.net/',
		SYNTAX_DOCUMENTATION: 'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
	}
	
	file_extensions = ('.rst', '.rest')
	default_extension = '.rst'
	
	@staticmethod
	def available():
		try:
			import docutils.core
		except:
			return False
		return True
	
	def __init__(self, filename=None):
		from docutils.core import publish_parts
		overrides = {'report_level': 4}
		self.publish_parts = lambda text: publish_parts(text,
			writer_name='html', settings_overrides=overrides)
	
	def get_document_title(self, text):
		return self.publish_parts(text)['title']
	
	def get_document_body(self, text):
		return self.publish_parts(text)['body']
	
	def get_stylesheet(self, text=''):
		orig_stylesheet = self.publish_parts(text)['stylesheet']
		# Cut off <style> and </style> tags
		return orig_stylesheet[25:-10]
	
	def get_javascript(self, text=''):
		head = self.publish_parts(text)['head']
		start_position = head.find('<script ')
		end_position = head.rfind('</script>')
		if start_position >= 0 and end_position >= 0:
			return head[start_position:end_position+9]+'\n'
		return ''

known_markups = (MarkdownMarkup, ReStructuredTextMarkup)

def get_available_markups():
	available_markups = []
	for markup in known_markups:
		if markup.available():
			available_markups.append(markup)
	return available_markups

def get_markup_for_file_name(filename, return_class=False):
	markup_class = None
	for markup in known_markups:
		for extension in markup.file_extensions:
			if filename.endswith(extension):
				markup_class = markup
	if return_class:
		return markup_class
	if markup_class and markup_class.available():
		return markup_class(filename=filename)

def find_markup_class_by_name(name):
	for markup in known_markups:
		if markup.name.lower() == name.lower():
			return markup
