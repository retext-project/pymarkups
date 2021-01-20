.. image:: https://github.com/retext-project/pymarkups/workflows/tests/badge.svg
   :target: https://github.com/retext-project/pymarkups/actions
   :alt: GitHub Actions status
.. image:: https://codecov.io/gh/retext-project/pymarkups/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/retext-project/pymarkups
   :alt: Coverage status
.. image:: https://readthedocs.org/projects/pymarkups/badge/?version=latest
   :target: https://pymarkups.readthedocs.io/en/latest/
   :alt: ReadTheDocs status

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
  'https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html'
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

.. _Markdown: https://daringfireball.net/projects/markdown/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Textile: https://en.wikipedia.org/wiki/Textile_(markup_language)

The release version can be downloaded from PyPI_ or installed using::

  pip install Markups

.. _PyPI: https://pypi.org/project/Markups/

The source code is hosted on GitHub_.

.. _GitHub: https://github.com/retext-project/pymarkups

The documentation is available online_ or can be generated from source by
installing Sphinx_ and running::

  python3 setup.py build_sphinx

.. _online: https://pymarkups.readthedocs.io/en/latest/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
