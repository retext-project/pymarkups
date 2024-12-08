# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2024

from __future__ import annotations

from typing import Any

import markups.common as common
from markups.abstract import AbstractMarkup, ConvertedMarkup

try:
    from docutils.core import publish_parts
    from docutils.writers.html5_polyglot import HTMLTranslator, Writer

    HAVE_DOCUTILS = True
except ImportError:
    HAVE_DOCUTILS = False

if HAVE_DOCUTILS:

    class CustomHTMLTranslator(HTMLTranslator):  # type: ignore
        def starttag(  # type: ignore
            self,
            node,
            tagname,
            suffix="\n",
            empty=False,
            **attributes,
        ):
            if getattr(node, "line", None) is not None:
                attributes["data-posmap"] = node.line
            return super().starttag(node, tagname, suffix, empty, **attributes)


class ReStructuredTextMarkup(AbstractMarkup):
    """Markup class for reStructuredText language.
    Inherits :class:`~markups.abstract.AbstractMarkup`.

    :param settings_overrides: optional dictionary of overrides for the
                               `Docutils settings`_
    :type settings_overrides: dict

    .. _`Docutils settings`: https://docutils.sourceforge.io/docs/user/config.html
    """

    name = "reStructuredText"
    attributes = {
        common.LANGUAGE_HOME_PAGE: "https://docutils.sourceforge.io/rst.html",
        common.MODULE_HOME_PAGE: "https://docutils.sourceforge.io/",
        common.SYNTAX_DOCUMENTATION: "https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html",
    }

    file_extensions = (".rst", ".rest")
    default_extension = ".rst"

    @staticmethod
    def available() -> bool:
        return HAVE_DOCUTILS

    def __init__(
        self,
        filename: str | None = None,
        settings_overrides: dict[str, Any] | None = None,
    ):
        self.overrides = settings_overrides or {}
        self.overrides.update(
            {
                "math_output": "MathJax " + common.MATHJAX_WEB_URL,
                "syntax_highlight": "short",
                "halt_level": 5,  # Never convert system messages to exceptions
                "stylesheet_path": "minimal.css",  # Do not include plain.css
            },
        )
        AbstractMarkup.__init__(self, filename)
        self.writer = Writer()
        self.writer.translator_class = CustomHTMLTranslator

    def convert(self, text: str) -> ConvertedReStructuredText:
        parts = publish_parts(
            text,
            source_path=self.filename,
            writer=self.writer,
            settings_overrides=self.overrides,
        )

        # Determine head
        head = parts["head"]

        # Determine body
        body = parts["html_body"]

        # Determine title
        title = parts["title"]

        # Determine stylesheet
        origstyle = parts["stylesheet"]
        # Cut off <style> and </style> tags
        stylestart = '<style type="text/css">'
        stylesheet = ""
        if stylestart in origstyle:
            stylesheet = origstyle[
                origstyle.find(stylestart) + 25 : origstyle.rfind("</style>")
            ]
        stylesheet += common.get_pygments_stylesheet(".code")

        return ConvertedReStructuredText(head, body, title, stylesheet)


class ConvertedReStructuredText(ConvertedMarkup):
    def __init__(self, head: str, body: str, title: str, stylesheet: str):
        ConvertedMarkup.__init__(self, body, title, stylesheet)
        self.head = head

    def get_javascript(self, webenv: bool = False) -> str:
        if common.MATHJAX_WEB_URL not in self.head:
            return ""
        mathjax_url, mathjax_version = common.get_mathjax_url_and_version(webenv)
        if mathjax_version == 2:
            mathjax_url += "?config=TeX-AMS_CHTML"
        async_attr = " async" if mathjax_version == 3 else ""
        script_tag = '<script type="text/javascript" src="%s"%s></script>\n'
        return script_tag % (mathjax_url, async_attr)
