# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dave Kuhlman, 2022

import importlib
import warnings
from io import StringIO

import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup


class AsciiDocMarkup(AbstractMarkup):
    """Markup class for AsciiDoc language.
    Inherits :class:`~markups.abstract.AbstractMarkup`.
    """

    name = "asciidoc"
    attributes = {
        common.LANGUAGE_HOME_PAGE: "https://asciidoc.org",
        common.MODULE_HOME_PAGE: "https://asciidoc-py.github.io",
        common.SYNTAX_DOCUMENTATION: "https://asciidoc-py.github.io/userguide.html",
    }

    file_extensions = (".adoc", ".asciidoc")
    default_extension = ".adoc"

    @staticmethod
    def available() -> bool:
        try:
            importlib.import_module("asciidoc")
            importlib.import_module("lxml")
        except ImportError:
            return False
        return True

    def convert(self, text: str) -> ConvertedMarkup:
        import asciidoc
        from lxml import etree

        outfile = StringIO()
        infile = StringIO(text)
        opts = [
            ("--backend", "html5"),
            ("--attribute", r"newline=\n"),
            ("--attribute", "footer-style=none"),
            ("--out-file", outfile),
        ]
        try:
            asciidoc.execute(None, opts, [infile])
        except SystemExit as ex:
            warnings.warn(str(ex.__context__), SyntaxWarning)
            pass
        result = outfile.getvalue()
        parser = etree.HTMLParser()
        root_element = etree.fromstring(result, parser)
        head_element = root_element.xpath("./head")[0]
        title_element = root_element.xpath("./head/title")[0]
        style_elements = root_element.xpath("./head/style")
        javascript_elements = root_element.xpath("./head/script")
        body_element = root_element.xpath("./body")[0]
        head = ""
        for child in head_element.getchildren():
            head += etree.tostring(
                child,
                encoding="unicode",
                method="html",
            )
        body = ""
        for child in body_element.getchildren():
            body += etree.tostring(
                child,
                encoding="unicode",
                method="html",
            )
        title = title_element.text
        stylesheet = ""
        for style_element in style_elements:
            stylesheet += style_element.text
        javascript = ""
        for javascript_element in javascript_elements:
            javascript += etree.tostring(
                javascript_element,
                encoding="unicode",
                method="html",
            )
        return ConvertedMarkup(body, title, stylesheet, javascript)
