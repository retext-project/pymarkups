#!/usr/bin/python

from distutils.core import setup
import distutils.command.check

version = '0.2.1'

long_description = \
"""This module provides a wrapper around the various text markup languages,
such as Markdown_ and reStructuredText_ (these two are supported by default).

Usage example:

>>> markup = markups.get_markup_for_file_name("myfile.rst")
>>> markup.name
'reStructuredText'
>>> markup.attributes[markups.SYNTAX_DOCUMENTATION]
'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
>>> text = "Hello, world!\\n=============\\n\\nThis is an example **reStructuredText** document."
>>> markup.get_document_title(text)
'Hello, world!'
>>> markup.get_document_body(text)
'<p>This is an example <strong>reStructuredText</strong> document.</p>\\n'

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
"""

classifiers = ['Development Status :: 4 - Beta',
	'License :: OSI Approved :: BSD License',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.0',
	'Programming Language :: Python :: 3.1',
	'Programming Language :: Python :: 3.2',
	'Topic :: Text Processing :: Markup',
	'Topic :: Text Processing :: General',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

class run_tests(distutils.command.check.check):
	def run(self):
		distutils.command.check.check.run(self)
		import tests.test_public_api
		import tests.test_markdown
		import tests.test_restructuredtext
		import tests.test_web
		print('test_markdown: testing extensions loading')
		tests.test_markdown.test_extensions_loading()
		print('test_markdown: testing markdown extra')
		tests.test_markdown.test_extra()
		print('test_markdown: testing markdown without extra')
		tests.test_markdown.test_remove_extra()
		print('test_markdown: testing meta extension')
		tests.test_markdown.test_meta()
		print('test_markdown: testing mathjax extension')
		tests.test_markdown.test_mathjax()
		print('test_restructuredtext: testing math loading')
		tests.test_restructuredtext.test_mathjax_loading()
		print('test_web: testing markups.web module')
		tests.test_web.test_web()
		print('test_public_api: testing public API')
		tests.test_public_api.test_api()

setup(name='Markups',
	version=version,
	description='A wrapper around various text markups',
	long_description=long_description,
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='http://launchpad.net/python-markups',
	packages=['markups'],
	license='BSD',
	classifiers=classifiers,
	cmdclass={'check': run_tests},
)
