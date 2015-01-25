# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import os
import sys
import unittest
from markups.restructuredtext import ReStructuredTextMarkup

if sys.version_info[0] < 3:
	raise unittest.SkipTest('Python 3.x is required')

import markups.web

class WebTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		if os.path.exists('tests/data'):
			working_dir='tests/data'
		elif os.path.exists('data'):
			working_dir='data'
		else:
			raise RuntimeError('Could not find data directory!')
		cls.get_file = staticmethod(lambda fn: os.path.join(working_dir, fn))
		app_data = ('test', '1.0', 'http://example.com/')
		cls.lib = markups.web.WebLibrary(working_dir, app_data)

	@unittest.skipUnless(ReStructuredTextMarkup.available(), 'Docutils not available')
	def test_web(self):
		self.lib.update('page.rst')
		with open(self.get_file('page.html')) as expected_file:
			expected_output = expected_file.read()
		with open(self.get_file('html/page.html')) as html_file:
			html_output = html_file.read()
		self.assertEqual(expected_output, html_output)
		os.remove(self.get_file('html/page.html'))
		self.lib.update_all()
		self.assertTrue(os.path.exists(self.get_file('html/page.html')))

	def test_exceptions(self):
		self.assertRaisesRegex(markups.web.WebUpdateError,
			'File not found.', self.lib.update, 'nosuchfile.txt')
		with open(self.get_file('test.unknown'), 'w'):
			pass
		self.assertRaisesRegex(markups.web.WebUpdateError,
			'No suitable markup found.', self.lib.update,
			'test.unknown')
		os.remove(self.get_file('test.unknown'))

	@classmethod
	def tearDownClass(cls):
		if os.path.exists(cls.get_file('html/page.html')):
			os.remove(cls.get_file('html/page.html'))
		if os.path.exists(cls.get_file('html')):
			os.rmdir(cls.get_file('html'))

if __name__ == '__main__':
	unittest.main()
