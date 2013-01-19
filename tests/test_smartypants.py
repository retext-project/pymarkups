# -*- coding: utf-8 -*-

# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups.common import educate as ed
import unittest

class SmartyTest(unittest.TestCase):
	def test_quotes(self):
		self.assertEqual(ed('"Isn\'t this fun?"'), '“Isn’t this fun?”')
		self.assertEqual(ed('"\'Quoted\' words in a larger quote."'),
			'“‘Quoted’ words in a larger quote.”')
	
	def test_dates(self):
		self.assertEqual(ed("1440--80's"), "1440–80’s")
		self.assertEqual(ed("'80s"), "‘80s")
	
	def test_ellipses_and_dashes(self):
		self.assertEqual(ed('em-dashes (---) and ellipes (...)'),
			'em-dashes (—) and ellipes (…)')

if __name__ == '__main__':
	unittest.main()
