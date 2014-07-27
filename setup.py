#!/usr/bin/python

import sys
from distutils.core import setup, Command
from markups import __version__ as version

try:
	from sphinx.setup_command import BuildDoc
except ImportError:
	BuildDoc = None

try:
	from setuptools.command.upload_docs import upload_docs
except ImportError:
	upload_docs = None

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
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Topic :: Text Processing :: Markup',
	'Topic :: Text Processing :: General',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

class run_tests(Command):
	user_options = []

	def initialize_options(self): pass
	def finalize_options(self): pass

	def run(self):
		import tests
		oldargv, sys.argv = sys.argv, ['setup.py test', '-v']
		try:
			tests.main()
		except SystemExit as e:
			if e.code:
				raise
		sys.argv = oldargv

cmdclass = {}
if sys.version_info[0] >= 3:
	cmdclass['test'] = run_tests
if BuildDoc:
	cmdclass['build_sphinx'] = BuildDoc
if upload_docs:
	cmdclass['upload_docs'] = upload_docs

setup_args = {
	'name': 'Markups',
	'version': version,
	'description': 'A wrapper around various text markups',
	'long_description': long_description,
	'author': 'Dmitry Shachnev',
	'author_email': 'mitya57@gmail.com',
	'url': 'https://github.com/mitya57/pymarkups',
	'packages': ['markups'],
	'license': 'BSD',
	'cmdclass': cmdclass,
	'classifiers': classifiers
}
setup(**setup_args)
