# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups import MarkdownMarkup
import os
import sys

tables_source = \
'''th1 | th2
--- | ---
t11 | t21
t12 | t22'''

tables_output = \
'''<table>
<thead>
<tr>
<th>th1</th>
<th>th2</th>
</tr>
</thead>
<tbody>
<tr>
<td>t11</td>
<td>t21</td>
</tr>
<tr>
<td>t12</td>
<td>t22</td>
</tr>
</tbody>
</table>
'''

deflists_source = \
'''Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.'''

deflists_output = \
'''<dl>
<dt>Apple</dt>
<dd>Pomaceous fruit of plants of the genus Malus in 
the family Rosaceae.</dd>
<dt>Orange</dt>
<dd>The fruit of an evergreen tree of the genus Citrus.</dd>
</dl>
'''

def create_extensions_txt(extensions_list):
	extensions_txt = open('markdown-extensions.txt', 'w')
	for extension in extensions_list:
		extensions_txt.write(extension+'\n')
	extensions_txt.close()

def fail_test(message):
	sys.exit('Markdown test failed: '+message)

def test_extensions_loading():
	markup = MarkdownMarkup()
	if markup._check_extension_exists('nonexistent'):
		fail_test('failed to detect nonexistent extension')
	if not markup._check_extension_exists('meta'):
		fail_test('meta extension marked as nonexistent')

def test_extra():
	markup = MarkdownMarkup()
	html = markup.get_document_body(tables_source)
	if html != tables_output:
		sys.stderr.write(html)
		fail_test('tables extension not working')
	html = markup.get_document_body(deflists_source)
	if html != deflists_output:
		sys.stderr.write(html)
		fail_test('def_list extension not working')

def test_remove_extra():
	create_extensions_txt(['remove_extra'])
	markup = MarkdownMarkup()
	html = markup.get_document_body(tables_source)
	os.remove('markdown-extensions.txt')
	if html == tables_output:
		fail_test('remove_extra not working')

def test_meta():
	create_extensions_txt(['meta'])
	markup = MarkdownMarkup()
	os.remove('markdown-extensions.txt')
	title = markup.get_document_title('Title: Hello, world!\n\nSome text here.')
	if title != 'Hello, world!':
		fail_test('meta not working')

def test_mathjax():
	create_extensions_txt(['mathjax'])
	markup = MarkdownMarkup()
	os.remove('markdown-extensions.txt')
	if markup.get_javascript('Hello, world!'):
		fail_test('get_javascript() returned non-empty string')
	js = markup.get_javascript('Hello, $2+2$!')
	if not '<script' in js:
		fail_test('mathjax script not included')
	body = markup.get_document_body('Hello, $2+2$!')
	if body != '<p>Hello, <mathjax>$2+2$</mathjax>!</p>\n':
		fail_test('mathjax not working')

if __name__ == '__main__':
	test_extensions_loading()
	test_extra()
	test_remove_extra()
	test_meta()
	test_mathjax()
