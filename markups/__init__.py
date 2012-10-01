# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import sys
from markups.core import *
from markups.markdown import MarkdownMarkup
from markups.restructuredtext import ReStructuredTextMarkup

__version__ = '0.2.2'

builtin_markups = [MarkdownMarkup, ReStructuredTextMarkup]

# Public API

def get_custom_markups():
	try:	
		list_file = open(CONFIGURATION_DIR+'pymarkups.txt')
	except IOError:
		return []
	else:
		custom_markups_names = [line.rstrip() for line in list_file]
		custom_markups = []
		for markup_name in custom_markups_names:
			try:
				module = __import__('markups.'+markup_name, {}, {}, ['markups'])
			except ImportError:
				sys.stderr.write('Warning: cannot import module markups.'+markup_name+'\n')
			else:
				custom_markups.append(module.markup)
		return custom_markups

def get_all_markups():
	return builtin_markups + get_custom_markups()

def get_available_markups():
	available_markups = []
	for markup in get_all_markups():
		if markup.available():
			available_markups.append(markup)
	return available_markups

def get_markup_for_file_name(filename, return_class=False):
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
	for markup in get_all_markups():
		if markup.name.lower() == name.lower():
			return markup
