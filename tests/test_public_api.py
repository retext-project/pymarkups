# This file is part of python-markups test suite
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2022

import importlib
import unittest

import markups
from markups.common import get_pygments_stylesheet


class APITest(unittest.TestCase):
    def test_api(self) -> None:
        all_markups = markups.get_all_markups()
        self.assertIn(markups.MarkdownMarkup, all_markups)
        self.assertIn(markups.ReStructuredTextMarkup, all_markups)
        self.assertIn(markups.AsciiDocMarkup, all_markups)
        markup_class = markups.find_markup_class_by_name("restructuredtext")
        self.assertEqual(markups.ReStructuredTextMarkup, markup_class)
        markup_class = markups.get_markup_for_file_name("myfile.mkd", return_class=True)
        self.assertEqual(markups.MarkdownMarkup, markup_class)
        markup_class = markups.get_markup_for_file_name(
            "myfile.adoc",
            return_class=True,
        )
        self.assertEqual(markups.AsciiDocMarkup, markup_class)

    @unittest.skipUnless(markups.MarkdownMarkup.available(), "Markdown not available")
    def test_api_instance(self) -> None:
        markup = markups.get_markup_for_file_name("myfile.mkd")
        self.assertIsInstance(markup, markups.MarkdownMarkup)

    @unittest.skipUnless(markups.MarkdownMarkup.available(), "Markdown not available")
    def test_available_markups(self) -> None:
        available_markups = markups.get_available_markups()
        self.assertIn(markups.MarkdownMarkup, available_markups)

    def test_get_pygments_stylesheet(self) -> None:
        try:
            importlib.import_module("pygments.formatters")
        except ImportError:
            raise unittest.SkipTest("Pygments not available")
        stylesheet = get_pygments_stylesheet(".selector")
        self.assertIn(".selector .nf { color: #00F", stylesheet)
        stylesheet = get_pygments_stylesheet(".selector", style="colorful")
        self.assertIn(".selector .nf { color: #06B", stylesheet)
        self.assertFalse(get_pygments_stylesheet(".selector", style=""))
