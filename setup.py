#!/usr/bin/python

from distutils.core import setup

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

setup(name='Markups',
	version='0.2',
	description='A wrapper around various text markups',
	long_description=long_description,
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='http://launchpad.net/python-markups',
	packages=['markups'],
	license='BSD',
	classifiers=classifiers,
	requires=['dbus']
)
