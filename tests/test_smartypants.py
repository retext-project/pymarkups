# -*- coding: utf-8 -*-

# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from __future__ import unicode_literals

from markups.common import educate as ed
from markups import MarkdownMarkup
import unittest

class SmartyTest(unittest.TestCase):
	def test_quotes(self):
		self.assertEqual(ed('"Isn\'t this fun?"'), '“Isn’t this fun?”')
		self.assertEqual(ed('"\'Quoted\' words in a larger quote."'),
			'“‘Quoted’ words in a larger quote.”')
	
	def test_dates(self):
		self.assertEqual(ed("1440--80's"), "1440–80’s")
		self.assertEqual(ed("'80s"), "‘80s")
	
	def test_ellipses_and_dashes(self):
		self.assertEqual(ed('em-dashes (---) and ellipes (...)'),
			'em-dashes (—) and ellipes (…)')
	
	def test_markdown_converting(self):
		m = MarkdownMarkup()
		body = m.get_document_body('"It\'s cool, isn\'t it?" --- she said.')
		expected = '<p>“It’s cool, isn’t it?” — she said.</p>\n'
		self.assertEqual(body, expected)

expected_table_body = (
'''<table>
<thead>
<tr>
<th>Direction 1</th>
<th>Direction 2</th>
</tr>
</thead>
<tbody>
<tr>
<td>Rome — Paris</td>
<td>Paris — Rome</td>
</tr>
</tbody>
</table>
''')

expected_code_body = \
'''<pre><code>code with a "quote"
code with a --- dash
</code></pre>
'''

class SmartyMarkdownTest(unittest.TestCase):
	def setUp(self):
		self.m = MarkdownMarkup(extensions=[])
	
	def test_hr(self):
		body = self.m.get_document_body('---')
		self.assertEqual(body, '<hr>\n')
	
	def test_quotes(self):
		body = self.m.get_document_body(
			'"quoted" text and **bold "quoted" text**')
		self.assertEqual(body,
			'<p>“quoted” text and <strong>bold “quoted” text</strong></p>\n')
		body = self.m.get_document_body(r'escaped \"quoted\" text')
		self.assertEqual(body, '<p>escaped &#34;quoted&#34; text</p>\n')
	
	def test_tables(self):
		body = self.m.get_document_body(
			'Direction 1    | Direction 2\n'
			'-----------    | -----------\n'
			'Rome --- Paris | Paris --- Rome')
		self.assertEqual(body, expected_table_body)
	
	def test_code_blocks(self):
		body = self.m.get_document_body(
			'    code with a "quote"\n'
			'    code with a --- dash')
		self.assertEqual(body, expected_code_body)
	
	def test_mathjax(self):
		m = MarkdownMarkup(extensions=['mathjax'])
		body = m.get_document_body('$1 -- 2$ -- 3')
		self.assertEqual(body,
			'<p>\n<script type="math/tex">1 -- 2</script> – 3</p>\n')

if __name__ == '__main__':
	unittest.main()
