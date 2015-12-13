# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2015

import markups
import unittest

class APITest(unittest.TestCase):
	def test_api(self):
		all_markups = markups.get_all_markups()
		self.assertIn(markups.MarkdownMarkup, all_markups)
		self.assertIn(markups.ReStructuredTextMarkup, all_markups)
		markup_class = markups.find_markup_class_by_name('restructuredtext')
		self.assertEqual(markups.ReStructuredTextMarkup, markup_class)
		markup_class = markups.get_markup_for_file_name('myfile.mkd', return_class=True)
		self.assertEqual(markups.MarkdownMarkup, markup_class)

	@unittest.skipUnless(markups.MarkdownMarkup.available(), 'Markdown not available')
	def test_api_instance(self):
		markup = markups.get_markup_for_file_name('myfile.mkd')
		self.assertIsInstance(markup, markups.MarkdownMarkup)

if __name__ == '__main__':
	unittest.main()
