# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import markups.web
import os
import unittest

class WebTest(unittest.TestCase):
	def setUp(self):
		if os.path.exists('tests/data'):
			self.working_dir='tests/data'
		elif os.path.exists('data'):
			self.working_dir='data'
		else:
			raise RuntimeError('Could not find data directory!')
		self.get_file = lambda fn: os.path.join(self.working_dir, fn)
	
	def test_web(self):	
		app_data = ('test', '1.0', 'http://example.com/')
		lib = markups.web.WebLibrary(self.working_dir, app_data)
		lib.update('page.rst')
		expected_file = open(self.get_file('page.html'))
		expected_output = expected_file.read()
		expected_file.close()
		html_file = open(self.get_file('html/page.html'))
		html_output = html_file.read()
		html_file.close()
		self.assertEqual(expected_output, html_output)
		os.remove(self.get_file('html/page.html'))
		lib.update_all()
		self.assertTrue(os.path.exists(self.get_file('html/page.html')))
	
	def tearDown(self):
		os.remove(self.get_file('html/page.html'))
		os.rmdir(self.get_file('html'))

if __name__ == '__main__':
	unittest.main()
