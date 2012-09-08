# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import markups
import sys

def fail_test():
	sys.exit('Public API test failed: '+message)

def test_api():
	all_markups = markups.get_all_markups()
	if not (markups.MarkdownMarkup in all_markups and
	markups.ReStructuredTextMarkup in all_markups):
		fail_test('builtin markups missing in get_all_markups() function')
	markup_class = markups.find_markup_class_by_name('restructuredtext')
	if markup_class != markups.ReStructuredTextMarkup:
		fail_test('find_markup_class_by_name not working')
	markup_class = markups.get_markup_for_file_name('myfile.mkd', return_class=True)
	if markup_class != markups.MarkdownMarkup:
		fail_test('get_markup_for_file_name not working (return_class=True)')
	markup = markups.get_markup_for_file_name('myfile.mkd')
	if not isinstance(markup, markups.MarkdownMarkup):
		fail_test('get_markup_for_file_name not working')

if __name__ == '__main__':
	test_api()
