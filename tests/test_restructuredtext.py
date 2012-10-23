# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import sys
from markups import ReStructuredTextMarkup

basic_text = \
'''Hello, world!
=============

This is an example **reStructuredText** document.'''

def fail_test(message):
	sys.exit('reStructuredText test failed: '+message)

def test_basic():
	markup = ReStructuredTextMarkup()
	text = markup.get_document_body(basic_text)
	title = markup.get_document_title(basic_text)
	markup.enable_cache = True
	text_from_cache = markup.get_document_body(basic_text)
	title_from_cache = markup.get_document_title(basic_text)
	text_expected = \
	'<p>This is an example <strong>reStructuredText</strong> document.</p>\n'
	title_expected = 'Hello, world!'
	if text != text_expected or text_from_cache != text_expected:
		fail_text('output does not match expexted')
	if title != title_expected or title_from_cache != title_expected:
		fail_text('title does not match expexted')

def test_mathjax_loading():
	markup = ReStructuredTextMarkup()
	if markup.get_javascript('Hello, world!'):
		fail_test('get_javascript() returned non-empty string')
	js = markup.get_javascript('Hello, :math:`2+2`!')
	if not '<script' in js:
		fail_test('mathjax script not included')
	body = markup.get_document_body('Hello, :math:`2+2`!')
	if not ('<span class="math">' in body and r'\(2+2\)</span>' in body):
		fail_test('math not working')

if __name__ == '__main__':
	test_basic()
	test_mathjax_loading()
