.. image:: https://api.travis-ci.org/retext-project/pymarkups.svg
   :target: https://travis-ci.org/retext-project/pymarkups
   :alt: Travis CI status

This module provides a wrapper around various text markup languages.

Available by default are Markdown_, reStructuredText_ and Textile_, but you
can easily add your own markups.

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
  >>> result = markup.convert(text)
  >>> result.get_document_title()
  'Hello, world!'
  >>> print(result.get_document_body())  # doctest: +NORMALIZE_WHITESPACE
  <div class="document" id="hello-world">
  <h1 class="title">Hello, world!</h1>
  <p>This is an example <strong>reStructuredText</strong> document.</p>
  </div>

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Textile: https://en.wikipedia.org/wiki/Textile_(markup_language)

The release version can be downloaded from PyPI_. The source code is hosted on
GitHub_.

.. _PyPI: https://pypi.python.org/pypi/Markups
.. _GitHub: https://github.com/retext-project/pymarkups

The documentation is available online_ or can be generated from source by
installing Sphinx_ and running::

  python3 setup.py build_sphinx

.. _online: https://pythonhosted.org/Markups/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
