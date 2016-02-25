# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2013

from markups import TextileMarkup
import unittest

@unittest.skipUnless(TextileMarkup.available(), 'Textile not available')
class TextileTest(unittest.TestCase):
	def test_textile(self):
		markup = TextileMarkup()
		html = markup.convert('Hello, **world**!').get_document_body()
		self.assertEqual(html, '\t<p>Hello, <b>world</b>!</p>')

if __name__ == '__main__':
	unittest.main()
