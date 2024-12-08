# This file is part of python-markups test suite
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dave Kuhlman, 2022

import unittest

from markups.asciidoc import AsciiDocMarkup


@unittest.skipUnless(
    AsciiDocMarkup.available(),
    "asciidoc.py and/or lxml not available",
)
class AsciiDocTextTest(unittest.TestCase):
    def test_basic(self) -> None:
        self.maxDiff = None
        markup = AsciiDocMarkup()
        converted = markup.convert(BASIC_TEXT)
        body = converted.get_document_body()
        title = converted.get_document_title()
        stylesheet = converted.get_stylesheet()
        title_expected = "Hello, world!"
        self.assertIn(CONTENT_PART_EXPECTED, body)
        self.assertEqual(title_expected, title)
        self.assertGreater(len(stylesheet), 100)

    def test_error_handling(self) -> None:
        markup = AsciiDocMarkup()
        with self.assertWarnsRegex(
            SyntaxWarning,
            "section title not allowed in list item",
        ):
            converted = markup.convert(INVALID_SYNTAX)
        self.assertIn("Foo", converted.get_document_body())

    def test_unicode(self) -> None:
        markup = AsciiDocMarkup()
        converted = markup.convert("Тест")
        body = converted.get_document_body()
        self.assertIn("Тест", body)


#
# =================================================================
#
# Data to be used for comparison of correct results.
#

BASIC_TEXT = """\
= Hello, world!
:toc:

== Some subtitle

This is an example *asciidoc* document.
"""

CONTENT_PART_EXPECTED = """\
<div id="content">
<div class="sect1">
<h2 id="_some_subtitle">Some subtitle</h2>
<div class="sectionbody">
<div class="paragraph"><p>This is an example <strong>asciidoc</strong> document.</p></div>
</div>
</div>
</div>
"""  # noqa: E501

INVALID_SYNTAX = """\
- Foo
+
= Bar
"""
