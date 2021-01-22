================
Built-in markups
================

These markups are available by default:

Markdown markup
===============

Markdown_ markup uses Python-Markdown_ as a backend (version 2.6 or later
is required).

There are several ways to enable `Python-Markdown extensions`_.

* List extensions in a file named :file:`markdown-extensions.yaml` or
  :file:`markdown-extensions.txt` in the :ref:`configuration directory
  <configuration-directory>`. The extensions will be automatically applied
  to all documents.
* If :file:`markdown-extensions.yaml` or :file:`markdown-extensions.txt`
  is placed into working directory, all documents in that directory will
  get extensions that are listed in that file.
* If first line of a document contains ":samp:`Required extensions:
  {ext1 ext2 ...}`", that list will be applied to a document.
* Finally, one can programmatically pass list of extension names to
  :class:`markups.MarkdownMarkup` constructor.

The YAML file should be a list of extensions, possibly with configuration
options, for example:

.. code-block:: yaml

   - smarty:
       substitutions:
         left-single-quote: "&sbquo;"
         right-single-quote: "&lsquo;"
       smart_dashes: False
   - toc:
       permalink: True
       separator: "_"
       toc_depth: 3
   - sane_lists

Or using a JSON-like syntax:

.. code-block:: yaml

   ["smarty", "sane_lists"]

YAML support works only when the PyYAML_ module is installed.

The txt file is a simple list of extensions, separated by newlines. Lines
starting with ``#`` are treated as comments and ignored. It is possible to
specify string options in brackets, for example::

   toc(title=Contents)
   sane_lists

The same syntax to specify options works in the ``Required extensions``
line. You can put it into a comment to make it invisible in the output::

   <!-- Required extensions: toc(title=Contents) sane_lists -->

The `Math Markdown extension`_ is enabled by default. This extension
supports a syntax for LaTeX-style math formulas (powered by MathJax_).
The delimiters are:

================  ===============
Inline math       Standalone math
================  ===============
``$...$`` [#f1]_  ``$$...$$``
``\(...\)``       ``\[...\]``
================  ===============

.. [#f1] To enable single-dollar-sign delimiter, one should add
   ``mdx_math(enable_dollar_delimiter=1)`` to the extensions list.

The `Python-Markdown Extra`_ set of extensions is enabled by default.
To disable it, one can enable virtual ``remove_extra`` extension
(which also completely disables LaTeX formulas support).

The default file extension associated with Markdown markup is ``.mkd``,
though many other extensions (including ``.md`` and ``.markdown``) are
supported as well.

.. _Markdown: https://daringfireball.net/projects/markdown/
.. _Python-Markdown: https://python-markdown.github.io/
.. _MathJax: https://www.mathjax.org/
.. _`Python-Markdown extensions`: https://python-markdown.github.io/extensions/
.. _PyYAML: https://pypi.org/project/PyYAML/
.. _`Math Markdown extension`: https://github.com/mitya57/python-markdown-math
.. _`Python-Markdown Extra`: https://python-markdown.github.io/extensions/extra/

.. autoclass:: markups.MarkdownMarkup

reStructuredText markup
========================

This markup provides support for reStructuredText_ language (the language
this documentation is written in). It uses Docutils_ Python module.

The file extension associated with reStructuredText markup is ``.rst``.

.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Docutils: https://docutils.sourceforge.io/

.. autoclass:: markups.ReStructuredTextMarkup

Textile markup
==============

This markup provides support for Textile_ language. It uses python-textile_
module.

The file extension associated with Textile markup is ``.textile``.

.. _Textile: https://en.wikipedia.org/wiki/Textile_(markup_language)
.. _python-textile: https://github.com/textile/python-textile

.. autoclass:: markups.TextileMarkup
