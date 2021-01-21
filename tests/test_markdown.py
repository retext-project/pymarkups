# vim: ts=8:sts=8:sw=8:noexpandtab

# This file is part of python-markups test suite
# License: 3-clause BSD, see LICENSE file
# Copyright: (C) Dmitry Shachnev, 2012-2018

from markups.markdown import MarkdownMarkup, _canonicalized_ext_names
from os.path import join
from tempfile import TemporaryDirectory
import unittest
import warnings

try:
	import pymdownx
except ImportError:
	pymdownx = None

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
<script type="math/tex">i_1</script> some text $escaped$ <script type="math/tex">i_2</script>
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
<p>$$escaped$$ \[escaped]</p>
'''

mathjax_multiline_source = \
r'''
$$
\TeX
\LaTeX
$$
'''

mathjax_multiline_output = \
r'''<p>
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

	def setUp(self):
		warnings.simplefilter("ignore", Warning)

	def test_empty_file(self):
		markup = MarkdownMarkup()
		self.assertEqual(markup.convert('').get_document_body(), '\n')

	def test_extensions_loading(self):
		markup = MarkdownMarkup()
		self.assertIsNone(markup._canonicalize_extension_name('nonexistent'))
		self.assertIsNone(markup._canonicalize_extension_name('nonexistent(someoption)'))
		self.assertIsNone(markup._canonicalize_extension_name('.foobar'))
		self.assertEqual(markup._canonicalize_extension_name('meta'), 'markdown.extensions.meta')
		name, parameters = markup._split_extension_config('toc(anchorlink=1, foo=bar)')
		self.assertEqual(name, 'toc')
		self.assertEqual(parameters, {'anchorlink': '1', 'foo': 'bar'})

	def test_loading_extensions_by_module_name(self):
		markup = MarkdownMarkup(extensions=['markdown.extensions.footnotes'])
		source = ('Footnotes[^1] have a label and the content.\n\n'
		          '[^1]: This is a footnote content.')
		html = markup.convert(source).get_document_body()
		self.assertIn('<sup', html)
		self.assertIn('footnote-backref', html)

	def test_removing_duplicate_extensions(self):
		markup = MarkdownMarkup(extensions=['remove_extra', 'toc', 'markdown.extensions.toc'])
		self.assertEqual(len(markup.extensions), 1)
		self.assertIn('markdown.extensions.toc', markup.extensions)

	def test_extensions_parameters(self):
		markup = MarkdownMarkup(extensions=['toc(anchorlink=1)'])
		html = markup.convert('## Header').get_document_body()
		self.assertEqual(html,
			'<h2 id="header"><a class="toclink" href="#header">Header</a></h2>\n')
		self.assertEqual(_canonicalized_ext_names['toc'], 'markdown.extensions.toc')

	def test_document_extensions_parameters(self):
		markup = MarkdownMarkup(extensions=[])
		toc_header = '<!--- Required extensions: toc(anchorlink=1) --->\n\n'
		html = markup.convert(toc_header + '## Header').get_document_body()
		self.assertEqual(html, toc_header +
			'<h2 id="header"><a class="toclink" href="#header">Header</a></h2>\n')
		toc_header = '<!--- Required extensions: toc(title=Table of contents, baselevel=3) wikilinks --->\n\n'
		html = markup.convert(toc_header + '[TOC]\n\n# Header\n[[Link]]').get_document_body()
		self.assertEqual(html, toc_header +
			'<div class="toc"><span class="toctitle">Table of contents</span><ul>\n'
			'<li><a href="#header">Header</a></li>\n'
			'</ul>\n</div>\n'
			'<h3 id="header">Header</h3>\n'
			'<p><a class="wikilink" href="/Link/">Link</a></p>\n')

	def test_extra(self):
		markup = MarkdownMarkup()
		html = markup.convert(tables_source).get_document_body()
		self.assertEqual(tables_output, html)
		html = markup.convert(deflists_source).get_document_body()
		self.assertEqual(deflists_output, html)

	def test_remove_extra(self):
		markup = MarkdownMarkup(extensions=['remove_extra'])
		html = markup.convert(tables_source).get_document_body()
		self.assertNotIn('<table>', html)

	def test_remove_extra_document_extension(self):
		markup = MarkdownMarkup(extensions=[])
		html = markup.convert(
			'Required-Extensions: remove_extra\n\n' +
			tables_source).get_document_body()
		self.assertNotIn('<table>', html)

	def test_remove_extra_double(self):
		"""Removing extra twice should not cause a crash."""
		markup = MarkdownMarkup(extensions=['remove_extra'])
		markup.convert('Required-Extensions: remove_extra\n')

	def test_remove_extra_removes_mathjax(self):
		markup = MarkdownMarkup(extensions=['remove_extra'])
		html = markup.convert('$$1$$').get_document_body()
		self.assertNotIn('math/tex', html)

	def test_meta(self):
		markup = MarkdownMarkup()
		text = ('Required-Extensions: meta\n'
		        'Title: Hello, world!\n\n'
		        'Some text here.')
		title = markup.convert(text).get_document_title()
		self.assertEqual('Hello, world!', title)

	def test_default_math(self):
		# by default $...$ delimeter should be disabled
		markup = MarkdownMarkup(extensions=[])
		self.assertEqual('<p>$1$</p>\n', markup.convert('$1$').get_document_body())
		self.assertEqual('<p>\n<script type="math/tex; mode=display">1</script>\n</p>\n',
			markup.convert('$$1$$').get_document_body())

	def test_mathjax(self):
		markup = MarkdownMarkup(extensions=['mathjax'])
		# Escaping should work
		self.assertEqual('', markup.convert('Hello, \\$2+2$!').get_javascript())
		js = markup.convert(mathjax_source).get_javascript()
		self.assertIn('<script', js)
		body = markup.convert(mathjax_source).get_document_body()
		self.assertEqual(mathjax_output, body)

	def test_mathjax_document_extension(self):
		markup = MarkdownMarkup()
		text = mathjax_header + mathjax_source
		body = markup.convert(text).get_document_body()
		self.assertEqual(mathjax_header + mathjax_output, body)

	def test_mathjax_multiline(self):
		markup = MarkdownMarkup(extensions=['mathjax'])
		body = markup.convert(mathjax_multiline_source).get_document_body()
		self.assertEqual(mathjax_multiline_output, body)

	def test_mathjax_multilevel(self):
		markup = MarkdownMarkup()
		body = markup.convert(mathjax_multilevel_source).get_document_body()
		self.assertEqual(mathjax_multilevel_output, body)

	def test_mathjax_asciimath(self):
		markup = MarkdownMarkup(extensions=['mdx_math(use_asciimath=1)'])
		converted = markup.convert(r'\( [[a,b],[c,d]] \)')
		body = converted.get_document_body()
		self.assertIn('<script type="math/asciimath">', body)
		self.assertIn('<script type="text/javascript"', converted.get_javascript())

	def test_not_loading_sys(self):
		with self.assertWarnsRegex(ImportWarning, 'Extension "sys" does not exist.'):
			markup = MarkdownMarkup(extensions=['sys'])
		self.assertNotIn('sys', markup.extensions)

	def test_extensions_txt_file(self):
		with TemporaryDirectory() as tmpdirname:
			txtfilename = join(tmpdirname, "markdown-extensions.txt")
			with open(txtfilename, "w") as f:
				f.write("foo\n# bar\nbaz(arg=value)\n")
			markup = MarkdownMarkup(filename=join(tmpdirname, "foo.md"))
		self.assertEqual(markup.global_extensions,
		                 [("foo", {}), ("baz", {"arg": "value"})])

	def test_extensions_yaml_file(self):
		with TemporaryDirectory() as tmpdirname:
			yamlfilename = join(tmpdirname, "markdown-extensions.yaml")
			with open(yamlfilename, "w") as f:
				f.write('- smarty:\n'
				        '    substitutions:\n'
				        '      left-single-quote: "&sbquo;"\n'
				        '      right-single-quote: "&lsquo;"\n'
				        '    smart_dashes: False\n'
				        '- toc:\n'
				        '    permalink: True\n'
				        '    separator: "_"\n'
				        '    toc_depth: 3\n'
				        '- sane_lists\n')
			markup = MarkdownMarkup(filename=join(tmpdirname, "foo.md"))
		self.assertEqual(
			markup.global_extensions,
			[("smarty", {"substitutions": {"left-single-quote": "&sbquo;",
			                               "right-single-quote": "&lsquo;"},
			  "smart_dashes": False}),
			 ("toc", {"permalink": True, "separator": "_", "toc_depth": 3}),
			 ("sane_lists", {}),
			])

	def test_extensions_yaml_file_invalid(self):
		with TemporaryDirectory() as tmpdirname:
			yamlfilename = join(tmpdirname, "markdown-extensions.yaml")
			with open(yamlfilename, "w") as f:
				f.write('[this is an invalid YAML file')
			with self.assertWarns(SyntaxWarning) as cm:
				MarkdownMarkup(filename=join(tmpdirname, "foo.md"))
			self.assertIn("Failed parsing", str(cm.warning))
			self.assertIn("expected ',' or ']'", str(cm.warning))

	def test_codehilite(self):
		markup = MarkdownMarkup(extensions=["codehilite"])
		converted = markup.convert('    :::python\n    import foo')
		stylesheet = converted.get_stylesheet()
		self.assertIn(".codehilite .k {", stylesheet)
		body = converted.get_document_body()
		self.assertIn('<div class="codehilite">', body)

	def test_codehilite_custom_class(self):
		markup = MarkdownMarkup(extensions=["codehilite(css_class=myclass)"])
		converted = markup.convert('    :::python\n    import foo')
		stylesheet = converted.get_stylesheet()
		self.assertIn(".myclass .k {", stylesheet)
		body = converted.get_document_body()
		self.assertIn('<div class="myclass">', body)

	@unittest.skipIf(pymdownx is None, "pymdownx module is not available")
	def test_pymdownx_highlight(self):
		markup = MarkdownMarkup(extensions=["pymdownx.highlight"])
		converted = markup.convert('    import foo')
		stylesheet = converted.get_stylesheet()
		self.assertIn(".highlight .k {", stylesheet)
		body = converted.get_document_body()
		self.assertIn('<div class="highlight">', body)

	@unittest.skipIf(pymdownx is None, "pymdownx module is not available")
	def test_pymdownx_highlight_custom_class(self):
		markup = MarkdownMarkup(extensions=["pymdownx.highlight(css_class=myclass)"])
		converted = markup.convert('    import foo')
		stylesheet = converted.get_stylesheet()
		self.assertIn(".myclass .k {", stylesheet)
		body = converted.get_document_body()
		self.assertIn('<div class="myclass">', body)
