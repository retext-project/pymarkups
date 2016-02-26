# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2015

import importlib
import os
import warnings
from markups.common import CONFIGURATION_DIR
from markups.markdown import MarkdownMarkup
from markups.restructuredtext import ReStructuredTextMarkup
from markups.textile import TextileMarkup

__version_tuple__ = (2, 0, 0)
__version__ = '.'.join(map(str, __version_tuple__))

builtin_markups = [MarkdownMarkup, ReStructuredTextMarkup, TextileMarkup]

# Public API

def get_custom_markups():
	"""
	:returns: list of registered :doc:`custom markups <custom_markups>`
	:rtype: list of markup classes
	"""
	try:
		list_file = open(os.path.join(CONFIGURATION_DIR, 'pymarkups.txt'))
	except IOError:
		return []
	else:
		custom_markups_names = [line.rstrip() for line in list_file]
		custom_markups = []
		for markup_name in custom_markups_names:
			try:
				module = importlib.import_module(markup_name)
				custom_markups.append(module.markup)
			except (ImportError, AttributeError):
				warnings.warn('Warning: cannot import module %r.' %
					markup_name, ImportWarning)
		return custom_markups

def get_all_markups():
	"""
	:returns: list of all markups (both standard and custom ones)
	:rtype: list of markup classes
	"""
	return builtin_markups + get_custom_markups()

def get_available_markups():
	"""
	:returns: list of all available markups (markups whose
	          :meth:`~markups.abstract.AbstractMarkup.available`
	          method returns True)
	:rtype: list of markup classes
	"""
	available_markups = []
	for markup in get_all_markups():
		if markup.available():
			available_markups.append(markup)
	return available_markups

def get_markup_for_file_name(filename, return_class=False):
	"""
	:param filename: name of the file
	:type filename: str
	:param return_class: if true, this function will return
	                     a class rather than an instance
	:type return_class: bool

	:returns: a markup with
	          :attr:`~markups.abstract.AbstractMarkup.file_extensions`
                  attribute containing extension of `filename`, if found,
	          otherwise ``None``

	>>> import markups
	>>> markup = markups.get_markup_for_file_name('foo.mkd')
	>>> markup.convert('**Test**').get_document_body()
	'<p><strong>Test</strong></p>\\n'
	>>> markups.get_markup_for_file_name('bar.rst', return_class=True)
	<class 'markups.restructuredtext.ReStructuredTextMarkup'>
	"""
	markup_class = None
	for markup in get_all_markups():
		for extension in markup.file_extensions:
			if filename.endswith(extension):
				markup_class = markup
	if return_class:
		return markup_class
	if markup_class and markup_class.available():
		return markup_class(filename=filename)

def find_markup_class_by_name(name):
	"""
	:returns: a markup with
	          :attr:`~markups.abstract.AbstractMarkup.name`
	          attribute matching `name`, if found, otherwise ``None``
	:rtype: class

	>>> import markups
	>>> markups.find_markup_class_by_name('textile')
	<class 'markups.textile.TextileMarkup'>
	"""
	for markup in get_all_markups():
		if markup.name.lower() == name.lower():
			return markup
