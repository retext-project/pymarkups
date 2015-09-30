# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012-2015

import os.path

# Some common constants and functions
(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)
CONFIGURATION_DIR = (os.getenv('XDG_CONFIG_HOME') or os.getenv('APPDATA') or
	os.path.expanduser('~/.config'))
MATHJAX_LOCAL_URL = 'file:///usr/share/javascript/mathjax/MathJax.js'
MATHJAX_WEB_URL = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js'

PYGMENTS_STYLE = 'default'

def get_pygments_stylesheet(selector, style=None):
	if style is None:
		style = PYGMENTS_STYLE
	if style == '':
		return ''
	try:
		from pygments.formatters import HtmlFormatter
	except ImportError:
		return ''
	else:
		return HtmlFormatter(style=style).get_style_defs(selector) + '\n'

def get_mathjax_url(webenv):
	if os.path.exists(MATHJAX_LOCAL_URL[7:]) and not webenv:
		return MATHJAX_LOCAL_URL
	else:
		return MATHJAX_WEB_URL
