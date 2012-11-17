# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import markups
import unittest

class APITest(unittest.TestCase):
	def test_api(self):
		all_markups = markups.get_all_markups()
		self.assertTrue(markups.MarkdownMarkup in all_markups and
		markups.ReStructuredTextMarkup in all_markups)
		markup_class = markups.find_markup_class_by_name('restructuredtext')
		self.assertEqual(markups.ReStructuredTextMarkup, markup_class)
		markup_class = markups.get_markup_for_file_name('myfile.mkd', return_class=True)
		self.assertEqual(markups.MarkdownMarkup, markup_class)
		markup = markups.get_markup_for_file_name('myfile.mkd')
		self.assertTrue(isinstance(markup, markups.MarkdownMarkup))

if __name__ == '__main__':
	unittest.main()
