# This file is part of python-markups module
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

# SmartyPants license
# ===================

# Copyright (C) 2003 John Gruber
# http://daringfireball.net/
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name "SmartyPants" nor the names of its contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# This software is provided by the copyright holders and contributors "as
# is" and any express or implied warranties, including, but not limited
# to, the implied warranties of merchantability and fitness for a
# particular purpose are disclaimed. In no event shall the copyright
# owner or contributors be liable for any direct, indirect, incidental,
# special, exemplary, or consequential damages (including, but not
# limited to, procurement of substitute goods or services; loss of use,
# data, or profits; or business interruption) however caused and on any
# theory of liability, whether in contract, strict liability, or tort
# (including negligence or otherwise) arising in any way out of the use
# of this software, even if advised of the possibility of such damage.

# smartypants.py license
# ======================

# Copyright (C) 2003 Chad Miller
# http://web.chad.org/

# smartypants.py is a derivative work of SmartyPants.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# This software is provided by the copyright holders and contributors "as
# is" and any express or implied warranties, including, but not limited
# to, the implied warranties of merchantability and fitness for a
# particular purpose are disclaimed. In no event shall the copyright
# owner or contributors be liable for any direct, indirect, incidental,
# special, exemplary, or consequential damages (including, but not
# limited to, procurement of substitute goods or services; loss of use,
# data, or profits; or business interruption) however caused and on any
# theory of liability, whether in contract, strict liability, or tort
# (including negligence or otherwise) arising in any way out of the use
# of this software, even if advised of the possibility of such damage.

import re
import os.path

# Some common constants and functions
(LANGUAGE_HOME_PAGE, MODULE_HOME_PAGE, SYNTAX_DOCUMENTATION) = range(3)
CONFIGURATION_DIR = (os.environ.get('XDG_CONFIG_HOME') or
	os.path.expanduser('~/.config'))
MATHJAX_LOCAL_URL = 'file:///usr/share/javascript/mathjax/MathJax.js'
MATHJAX_WEB_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'

def get_pygments_stylesheet(selector):
	try:
		from pygments.formatters import HtmlFormatter
	except ImportError:
		return ''
	else:
		return HtmlFormatter().get_style_defs(selector) + '\n'

def get_mathjax_url(webenv):
	if os.path.exists(MATHJAX_LOCAL_URL[7:]) and not webenv:
		return MATHJAX_LOCAL_URL
	else:
		return MATHJAX_WEB_URL

##########################################
#  SmartyPants API for converting ASCII  #
#  quotes/dashes to proper Unicode ones  #
##########################################

# Constants for quote education.
punct_class = r"""[!"#\$\%'()*+,-.\/:;<=>?\@\[\\\]\^_`{|}~]"""
end_of_word_class = r"""[\s.,;:!?)]"""
close_class = r"""[^\ \t\r\n\[\{\(\-]"""
dec_dashes = r"""&#8211;|&#8212;"""

# Special case if the very first character is a quote
# followed by punctuation at a non-word-break. Close the quotes by brute force:
single_quote_start_re = re.compile(r"""^'(?=%s\\B)""" % (punct_class,))
double_quote_start_re = re.compile(r"""^"(?=%s\\B)""" % (punct_class,))

# Special case for double sets of quotes, e.g.:
#   <p>He said, "'Quoted' words in a larger quote."</p>
double_quote_sets_re = re.compile(r""""'(?=\w)""")
single_quote_sets_re = re.compile(r"""'"(?=\w)""")

# Special case for decade abbreviations (the '80s):
decade_abbr_re = re.compile(r"""\b'(?=\d{2}s)""")

# Get most opening double quotes:
opening_double_quotes_regex = re.compile(r"""
(
	\s          | # a whitespace char, or
	&nbsp;      | # a non-breaking space entity, or
	--          | # dashes, or
	&[mn]dash;  | # named dash entities
	%s          | # or decimal entities
	&\#x201[34];  # or hex
)
"       # the quote
(?=\w)  # followed by a word character
""" % (dec_dashes,), re.VERBOSE)

# Double closing quotes:
closing_double_quotes_regex = re.compile(r"""
#(%s)?  # character that indicates the quote should be closing
"
(?=%s)
""" % (close_class, end_of_word_class), re.VERBOSE)

closing_double_quotes_regex_2 = re.compile(r"""
(%s)  # character that indicates the quote should be closing
"
""" % (close_class,), re.VERBOSE)

# Get most opening single quotes:
opening_single_quotes_regex = re.compile(r"""
(
	\s          | # a whitespace char, or
	&nbsp;      | # a non-breaking space entity, or
	--          | # dashes, or
	&[mn]dash;  | # named dash entities
	%s          | # or decimal entities
	&\#x201[34];  # or hex
)
'       # the quote
(?=\w)  # followed by a word character
""" % (dec_dashes,), re.VERBOSE)

closing_single_quotes_regex = re.compile(r"""
(%s)
'
(?!\s | s\b | \d)
""" % (close_class,), re.VERBOSE)

closing_single_quotes_regex_2 = re.compile(r"""
(%s)
'
(\s | s\b)
""" % (close_class,), re.VERBOSE)

def educate_quotes(s):
	# Special case if the very first character is a quote
	# followed by punctuation at a non-word-break. Close the quotes
	# by brute force:
	s = single_quote_start_re.sub(chr(8217), s)
	s = double_quote_start_re.sub(chr(8221), s)

	# Special case for double sets of quotes, e.g.:
	# "'Quoted' words in a larger quote."
	s = double_quote_sets_re.sub(chr(8220)+chr(8216), s)
	s = single_quote_sets_re.sub(chr(8216)+chr(8220), s)

	# Special case for decade abbreviations (the '80s):
	s = decade_abbr_re.sub(chr(8217), s)

	s = opening_single_quotes_regex.sub(r'\1'+chr(8216), s)
	s = closing_single_quotes_regex.sub(r'\1'+chr(8217), s)
	s = closing_single_quotes_regex_2.sub(r'\1'+chr(8217), s)

	# Any remaining single quotes should be opening ones:
	s = s.replace("'", chr(8216))

	s = opening_double_quotes_regex.sub(r'\1'+chr(8220), s)
	s = closing_double_quotes_regex.sub(chr(8221), s)
	s = closing_double_quotes_regex_2.sub(r'\1'+chr(8221), s)

	# Any remaining quotes should be opening ones.
	return s.replace('"', chr(8220))

def educate_ellipses(s):
	return s.replace('...', chr(8230))

def educate_dashes_oldschool(s):
	return s.replace('---', chr(8212)).replace('--', chr(8211))

def educate(s, fixers='qed'):
	if 'q' in fixers:
		s = educate_quotes(s)
	if 'e' in fixers:
		s = educate_ellipses(s)
	if 'd' in fixers:
		s = educate_dashes_oldschool(s)
	return s
