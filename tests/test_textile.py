# This file is part of python-markups test suite
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2013-2018

from markups import TextileMarkup
import unittest

@unittest.skipUnless(TextileMarkup.available(), 'Textile not available')
class TextileTest(unittest.TestCase):
	def test_textile(self):
		markup = TextileMarkup()
		html = markup.convert('Hello, **world**!').get_document_body()
		self.assertEqual(html, '\t<p>Hello, <b>world</b>!</p>')
