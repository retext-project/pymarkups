# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2014

import unittest
from markups import ReStructuredTextMarkup

basic_text = \
'''Hello, world!
=============

Some subtitle
~~~~~~~~~~~~~

This is an example **reStructuredText** document.'''

@unittest.skipUnless(ReStructuredTextMarkup.available(), 'Docutils not available')
class ReStructuredTextTest(unittest.TestCase):
	def test_basic(self):
		markup = ReStructuredTextMarkup()
		converted = markup.convert(basic_text)
		text = converted.get_document_body()
		title = converted.get_document_title()
		stylesheet = converted.get_stylesheet()
		text_expected = ('<div class="document" id="hello-world">\n'
			'<h1 class="title">Hello, world!</h1>\n'
			'<h2 class="subtitle" id="some-subtitle">Some subtitle</h2>\n'
			'<p>This is an example <strong>reStructuredText</strong> document.</p>\n'
			'</div>\n')
		title_expected = 'Hello, world!'
		self.assertEqual(text_expected, text)
		self.assertEqual(title_expected, title)
		self.assertIn('.code', stylesheet)

	def test_mathjax_loading(self):
		markup = ReStructuredTextMarkup()
		self.assertEqual('', markup.convert('Hello, world!').get_javascript())
		js = markup.convert('Hello, :math:`2+2`!').get_javascript()
		self.assertIn('<script', js)
		body = markup.convert('Hello, :math:`2+2`!').get_document_body()
		self.assertIn('<span class="math">', body)
		self.assertIn(r'\(2+2\)</span>', body)

	def test_errors(self):
		markup = ReStructuredTextMarkup('/dev/null',
		                                settings_overrides = {'warning_stream': False})
		body = markup.convert('`').get_document_body() # unclosed role
		self.assertIn('system-message', body)
		self.assertIn('/dev/null', body)

	def test_errors_overridden(self):
		markup = ReStructuredTextMarkup('/dev/null',
		                                settings_overrides = {'report_level': 4})
		body = markup.convert('`').get_document_body() # unclosed role
		self.assertNotIn('system-message', body)

if __name__ == '__main__':
	unittest.main()
