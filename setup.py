#!/usr/bin/env python3

import sys
try:
	from setuptools import setup, Command
except ImportError:
	from distutils.core import setup, Command
from markups import __version__ as version

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
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Topic :: Text Processing :: Markup',
	'Topic :: Text Processing :: General',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

class run_tests(Command):
	user_options = []

	def initialize_options(self): pass
	def finalize_options(self): pass

	def run(self):
		from unittest.main import main
		testprogram = main(module=None, argv=sys.argv[:1], verbosity=2, exit=False)
		if not testprogram.result.wasSuccessful():
			sys.exit(1)

cmdclass = {}
if sys.version_info[0] >= 3:
	cmdclass['test'] = run_tests

setup_args = {
	'name': 'Markups',
	'version': version,
	'description': 'A wrapper around various text markups',
	'long_description': long_description,
	'author': 'Dmitry Shachnev',
	'author_email': 'mitya57@gmail.com',
	'url': 'https://github.com/retext-project/pymarkups',
	'packages': ['markups'],
	'license': 'BSD',
	'cmdclass': cmdclass,
	'classifiers': classifiers
}
setup(**setup_args)
