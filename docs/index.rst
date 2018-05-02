===================================
Python-Markups module documentation
===================================

Introduction to Python-Markups
==============================

Python-Markups is a module that provides unified interface for using
various markup languages, such as Markdown, reStructuredText, and
Textile. It is also possible for clients to create and register their
own markup languages.

The output language Python-Markups works with is HTML. Stylesheets and
JavaScript sections are supported.

The abstract interface that any markup implements is
:class:`~markups.abstract.AbstractMarkup`.

Contents
========

.. toctree::

   overview
   interface
   standard_markups
   custom_markups
   changelog

Links
=====

* Python-Markups source code is hosted on GitHub_.
* You can get the source tarball from PyPI_.
* It is also packaged in Debian_.

.. _GitHub: https://github.com/retext-project/pymarkups
.. _PyPI: https://pypi.org/project/Markups/
.. _Debian: https://packages.debian.org/sid/source/pymarkups
