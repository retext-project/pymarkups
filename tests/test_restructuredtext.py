# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import sys
from markups import ReStructuredTextMarkup

math_output = \
r'''<p>Hello, <span class="math">
\(2+2\)</span>
!</p>
'''

def fail_test(message):
	sys.exit('reStructuredText test failed: '+message)

def test_mathjax_loading():
	markup = ReStructuredTextMarkup()
	if markup.get_javascript('Hello, world!'):
		fail_test('get_javascript() returned non-empty string')
	js = markup.get_javascript('Hello, :math:`2+2`!')
	if not '<script' in js:
		fail_test('mathjax script not included')
	body = markup.get_document_body('Hello, :math:`2+2`!')
	if body != math_output:
		fail_test('math not working')

if __name__ == '__main__':
	test_mathjax_loading()
