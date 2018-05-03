#!/usr/bin/env python3

from setuptools import setup
from markups import __version__ as version
from os.path import dirname, join

with open(join(dirname(__file__), 'README.rst')) as readme_file:
	long_description = '\n' + readme_file.read()

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'License :: OSI Approved :: BSD License',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Topic :: Text Processing :: Markup',
	'Topic :: Text Processing :: General',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

setup_args = {
	'name': 'Markups',
	'version': version,
	'description': 'A wrapper around various text markups',
	'long_description': long_description,
	'author': 'Dmitry Shachnev',
	'author_email': 'mitya57@gmail.com',
	'url': 'https://github.com/retext-project/pymarkups',
	'packages': ['markups'],
	'extras_require': {
		'Markdown': ['Markdown>=2.6'],
		'reStructuredText': ['docutils'],
		'Textile': ['textile'],
		'highlighting': ['Pygments'],
	},
	'entry_points': {
		'pymarkups': [
			'markdown = markups.markdown:MarkdownMarkup',
			'restructuredtext = markups.restructuredtext:ReStructuredTextMarkup',
			'textile = markups.textile:TextileMarkup',
		],
	},
	'license': 'BSD',
	'classifiers': classifiers
}
setup(**setup_args)
