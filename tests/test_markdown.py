# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

from markups import MarkdownMarkup
import unittest

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

mathjax_header = \
'<!--- Type: markdown; Required extensions: mathjax --->\n\n'

mathjax_source = \
r'''$i_1$ some text \$escaped\$ $i_2$

\(\LaTeX\) \\(escaped\)

$$m_1$$ text $$m_2$$

\[m_3\] text \[m_4\]

\( \sin \alpha \) text \( \sin \beta \)

\[ \alpha \] text \[ \beta \]

\$$escaped\$$ \\[escaped\]
'''

mathjax_output = \
r'''<p>
<script type="math/tex">i_1</script> some text \$escaped\$ <script type="math/tex">i_2</script>
</p>
<p>
<script type="math/tex">\LaTeX</script> \(escaped)</p>
<p>
<script type="math/tex; mode=display">m_1</script> text <script type="math/tex; mode=display">m_2</script>
</p>
<p>
<script type="math/tex; mode=display">m_3</script> text <script type="math/tex; mode=display">m_4</script>
</p>
<p>
<script type="math/tex"> \sin \alpha </script> text <script type="math/tex"> \sin \beta </script>
</p>
<p>
<script type="math/tex; mode=display"> \alpha </script> text <script type="math/tex; mode=display"> \beta </script>
</p>
<p>\$$escaped\$$ \[escaped]</p>
'''

mathjax_multiline_source = \
r'''
$$
\TeX
\LaTeX
$$
'''

mathjax_multiline_output = \
'''<p>
<script type="math/tex; mode=display">
\TeX
\LaTeX
</script>
</p>
'''

mathjax_multilevel_source = \
r'''
\begin{equation*}
  \begin{pmatrix}
    1 & 0\\
    0 & 1
  \end{pmatrix}
\end{equation*}
'''

mathjax_multilevel_output = \
r'''<p>
<script type="math/tex; mode=display">\begin{equation*}
  \begin{pmatrix}
    1 & 0\\
    0 & 1
  \end{pmatrix}
\end{equation*}</script>
</p>
'''

@unittest.skipUnless(MarkdownMarkup.available(), 'Markdown not available')
class MarkdownTest(unittest.TestCase):
	maxDiff = None

	def test_empty_file(self):
		markup = MarkdownMarkup()
		self.assertEqual(markup.get_document_body(''), '\n')

	def test_extensions_loading(self):
		markup = MarkdownMarkup()
		self.assertIsNone(markup._canonicalize_extension_name('nonexistent'))
		self.assertIsNone(markup._canonicalize_extension_name('nonexistent(someoption)'))
		self.assertIsNone(markup._canonicalize_extension_name('.foobar'))
		self.assertEqual(markup._canonicalize_extension_name('meta'), 'markdown.extensions.meta')
		self.assertEqual(markup._canonicalize_extension_name('meta(someoption)'),
			'markdown.extensions.meta(someoption)')

	def test_loading_extensions_by_module_name(self):
		markup = MarkdownMarkup(extensions=['markdown.extensions.footnotes'])
		source = ('Footnotes[^1] have a label and the content.\n\n'
		          '[^1]: This is a footnote content.')
		html = markup.get_document_body(source)
		self.assertIn('<sup', html)
		self.assertIn('footnote-backref', html)

	def test_removing_duplicate_extensions(self):
		markup = MarkdownMarkup(extensions=['remove_extra', 'toc', 'markdown.extensions.toc'])
		self.assertEqual(len(markup.extensions), 1)
		self.assertIn('markdown.extensions.toc', markup.extensions)

	def test_extensions_parameters(self):
		markup = MarkdownMarkup(extensions=['toc(anchorlink=1)'])
		html = markup.get_document_body('## Header')
		self.assertEqual(html,
			'<h2 id="header"><a class="toclink" href="#header">Header</a></h2>\n')

	def test_document_extensions_parameters(self):
		markup = MarkdownMarkup(extensions=[])
		toc_header = '<!--- Required extensions: toc(anchorlink=1) --->\n\n'
		html = markup.get_document_body(toc_header + '## Header')
		self.assertEqual(html, toc_header +
			'<h2 id="header"><a class="toclink" href="#header">Header</a></h2>\n')

	def test_extra(self):
		markup = MarkdownMarkup()
		html = markup.get_document_body(tables_source)
		self.assertEqual(tables_output, html)
		html = markup.get_document_body(deflists_source)
		self.assertEqual(deflists_output, html)

	def test_remove_extra(self):
		markup = MarkdownMarkup(extensions=['remove_extra'])
		html = markup.get_document_body(tables_source)
		self.assertNotIn(html, '<table>')

	def test_remove_extra_document_extension(self):
		markup = MarkdownMarkup(extensions=[])
		html = markup.get_document_body(
			'Required-Extensions: remove_extra\n\n' +
			tables_source)
		self.assertNotIn(html, '<table>')

	def test_remove_extra_removes_mathjax(self):
		markup = MarkdownMarkup()
		html = markup.get_document_body('$$1$$')
		self.assertNotIn(html, 'math/tex')

	def test_meta(self):
		markup = MarkdownMarkup()
		text = ('Required-Extensions: meta\n'
		        'Title: Hello, world!\n\n'
		        'Some text here.')
		title = markup.get_document_title(text)
		self.assertEqual('Hello, world!', title)

	def test_default_math(self):
		# by default $...$ delimeter should be disabled
		markup = MarkdownMarkup(extensions=[])
		self.assertEqual('<p>$1$</p>\n', markup.get_document_body('$1$'))
		self.assertEqual('<p>\n<script type="math/tex; mode=display">1</script>\n</p>\n',
			markup.get_document_body('$$1$$'))

	def test_mathjax(self):
		markup = MarkdownMarkup(extensions=['mathjax'])
		# Escaping should work
		self.assertEqual('', markup.get_javascript('Hello, \\$2+2$!'))
		js = markup.get_javascript(mathjax_source)
		self.assertIn('<script', js)
		body = markup.get_document_body(mathjax_source)
		self.assertEqual(mathjax_output, body)

	def test_mathjax_document_extension(self):
		markup = MarkdownMarkup()
		text = mathjax_header + mathjax_source
		body = markup.get_document_body(text)
		self.assertEqual(mathjax_header + mathjax_output, body)

	def test_mathjax_multiline(self):
		markup = MarkdownMarkup(extensions=['mathjax'])
		body = markup.get_document_body(mathjax_multiline_source)
		self.assertEqual(mathjax_multiline_output, body)

	def test_mathjax_multilevel(self):
		markup = MarkdownMarkup()
		body = markup.get_document_body(mathjax_multilevel_source)
		self.assertEqual(mathjax_multilevel_output, body)

	@unittest.skipUnless(hasattr(unittest.TestCase, 'assertWarnsRegex'), 'assertWarnsRegex is not supported')
	def test_not_loading_sys(self):
		with self.assertWarnsRegex(ImportWarning, 'Extension "sys" does not exist.'):
			markup = MarkdownMarkup(extensions=['sys'])
		self.assertNotIn('sys', markup.extensions)

if __name__ == '__main__':
	unittest.main()
