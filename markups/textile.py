# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2013-2024

import importlib

import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup


class TextileMarkup(AbstractMarkup):
    """Markup class for Textile language.
    Inherits :class:`~markups.abstract.AbstractMarkup`.
    """

    name = "Textile"
    attributes = {
        common.LANGUAGE_HOME_PAGE: "https://textile-lang.com",
        common.MODULE_HOME_PAGE: "https://github.com/textile/python-textile",
        common.SYNTAX_DOCUMENTATION: "https://movabletype.org/documentation/author/textile-2-syntax.html",
    }

    file_extensions = (".textile",)
    default_extension = ".textile"

    @staticmethod
    def available() -> bool:
        try:
            importlib.import_module("textile")
        except ImportError:
            return False
        return True

    def __init__(self, filename: str | None = None):
        AbstractMarkup.__init__(self, filename)
        from textile import textile

        self.textile = textile

    def convert(self, text: str) -> ConvertedMarkup:
        return ConvertedMarkup(self.textile(text))
