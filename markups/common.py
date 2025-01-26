# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2024

import os.path

# Some common constants and functions
(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)
CONFIGURATION_DIR = (
    os.getenv("XDG_CONFIG_HOME")
    or os.getenv("APPDATA")
    or os.path.expanduser("~/.config")
)
MATHJAX2_LOCAL_FILES = (
    "/usr/share/javascript/mathjax/MathJax.js",  # Debian libjs-mathjax
    "/usr/share/mathjax2/MathJax.js",  # Arch Linux mathjax2
)
MATHJAX3_LOCAL_FILES = (
    "/usr/share/nodejs/mathjax-full/es5/tex-chtml.js",  # Debian node-mathjax-full
    "/usr/share/mathjax/tex-chtml.js",  # Arch Linux mathjax
)
MATHJAX_WEB_URL = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"

PYGMENTS_STYLE = "default"


def get_pygments_stylesheet(selector: str | None, style: str | None = None) -> str:
    if style is None:
        style = PYGMENTS_STYLE
    if style == "":
        return ""
    try:
        from pygments.formatters import HtmlFormatter
    except ImportError:
        return ""
    else:
        defs = HtmlFormatter(style=style).get_style_defs(selector)
        assert isinstance(defs, str)
        return defs + "\n"


def get_mathjax_url_and_version(webenv: bool) -> tuple[str, int]:
    if not webenv:
        for path in MATHJAX3_LOCAL_FILES:
            if os.path.exists(path):
                return f"file://{path}", 3
        for path in MATHJAX2_LOCAL_FILES:
            if os.path.exists(path):
                return f"file://{path}", 2
    return MATHJAX_WEB_URL, 3
