.. image:: https://api.travis-ci.org/retext-project/pymarkups.svg
   :target: https://travis-ci.org/retext-project/pymarkups
   :alt: Travis CI status

This module provides a wrapper around the various text markup languages,
such as Markdown_ and reStructuredText_ (these two are supported by default).

Usage example:

.. code:: python

  >>> import markups
  >>> markup = markups.get_markup_for_file_name("myfile.rst")
  >>> markup.name
  'reStructuredText'
  >>> markup.attributes[markups.common.SYNTAX_DOCUMENTATION]
  'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
  >>> text = """
  ... Hello, world!
  ... =============
  ...
  ... This is an example **reStructuredText** document.
  ... """
  >>> markup.get_document_title(text)
  'Hello, world!'
  >>> markup.get_document_body(text)
  '<p>This is an example <strong>reStructuredText</strong> document.</p>\n'

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

The release version can be downloaded from PyPI_.

.. _PyPI: http://pypi.python.org/pypi/Markups
