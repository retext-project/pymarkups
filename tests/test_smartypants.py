# -*- coding: utf-8 -*-

# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups.common import educate as ed
import unittest

try:
	u = lambda s: unicode(s, 'utf-8') # For Python 2
except NameError:
	u = lambda s: s

class SmartyTest(unittest.TestCase):
	def test_quotes(self):
		self.assertEqual(ed('"Isn\'t this fun?"'), u('“Isn’t this fun?”'))
		self.assertEqual(ed('"\'Quoted\' words in a larger quote."'),
			u('“‘Quoted’ words in a larger quote.”'))
	
	def test_dates(self):
		self.assertEqual(ed("1440--80's"), u("1440–80’s"))
		self.assertEqual(ed("'80s"), u("‘80s"))
	
	def test_ellipses_and_dashes(self):
		self.assertEqual(ed('em-dashes (---) and ellipes (...)'),
			u('em-dashes (—) and ellipes (…)'))

if __name__ == '__main__':
	unittest.main()
