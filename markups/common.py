# This file is part of python-markups module
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2018

import os.path

# Some common constants and functions
(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)
CONFIGURATION_DIR = (os.getenv('XDG_CONFIG_HOME') or os.getenv('APPDATA') or
	os.path.expanduser('~/.config'))
MATHJAX_LOCAL_URLS = (
	'file:///usr/share/javascript/mathjax/MathJax.js',  # Debian libjs-mathjax
	'file:///usr/share/mathjax/MathJax.js',  # Arch Linux mathjax
)
MATHJAX_WEB_URL = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js'

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
	if not webenv:
		for url in MATHJAX_LOCAL_URLS:
			if os.path.exists(url[7:]):  # strip file://
				return url
	return MATHJAX_WEB_URL
