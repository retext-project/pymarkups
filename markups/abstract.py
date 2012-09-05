# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups.core import *

class AbstractMarkup(object):
	"""Abstract class for markup languages"""
	
	file_extensions = ()
	
	def available():
		return True
	
	def get_document_title(self, text):
		return ''
	
	def get_document_body(self, text):
		raise NotImplementedError()
	
	def get_stylesheet(self, text=''):
		return ''
	
	def get_javascript(self, text='', webenv=False):
		return ''
	
	def get_whole_html(self, text, custom_headers='', include_stylesheet=True,
	                   fallback_title='', webenv=False):
		stylesheet = ('<style type="text/css">\n' + self.get_stylesheet(text) +
			'</style>\n' if include_stylesheet else '')
		title = self.get_document_title(text)
		if not title:
			title = fallback_title
		title_string = ('<title>' + title + '</title>\n') if title else ''
		body = self.get_document_body(text)
		return (
		'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
		'<html>\n<head>\n'
		'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n'
		+ custom_headers + title_string + stylesheet +
		self.get_javascript(text, webenv) + '</head>\n<body>\n'
		+ body + '</body>\n</html>\n'
		)
