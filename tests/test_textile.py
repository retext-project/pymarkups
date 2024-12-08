# This file is part of python-markups test suite
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2013-2022

import unittest

from markups import TextileMarkup


@unittest.skipUnless(TextileMarkup.available(), "Textile not available")
class TextileTest(unittest.TestCase):
    def test_textile(self) -> None:
        markup = TextileMarkup()
        html = markup.convert("Hello, **world**!").get_document_body()
        self.assertEqual(html, "\t<p>Hello, <b>world</b>!</p>")
