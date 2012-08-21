# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import os.path

# Some common constants and functions
(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)
CONFIGURATION_DIR = os.path.expanduser('~/.config/')

def get_pygments_stylesheet(selector):
	try:
		from pygments.formatters import HtmlFormatter
	except:
		return ''
	else:
		return HtmlFormatter().get_style_defs(selector) + '\n'
