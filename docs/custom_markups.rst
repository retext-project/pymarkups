==============
Custom Markups
==============

Registering the markup module
=============================

Any third-party markup should be placed in the same directory
as built-in markups. To get that directory, use:

>>> import markups
>>> print(markups.__path__)

Every module should have :data:`markup` property pointing to
the markup class.

To register the markup, one should append the markup name to
file named ``pymarkups.txt`` in the
:ref:`configuration directory <configuration-directory>`.

To check if the module was found by Python-Markups, one can check
if the module is present in return value of
:func:`~markups.get_custom_markups` function.

Importing third-party modules
=============================

A markup must not directly import any third party Python module it uses
at file level. Instead, it should check the module availability in
:meth:`~markups.abstract.AbstractMarkup.available` static method.

That method can try to import the needed modules, and return ``True`` in
case of success, and ``False`` in case of failure.

Implementing methods
====================

Any markup must inherit from :class:`~markups.abstract.AbstractMarkup`
class.

Third-party markups must implement
:meth:`~markups.abstract.AbstractMarkup.get_document_body` method, which
is the main method of any markup.

Other methods that are optional:

 * :meth:`~markups.abstract.AbstractMarkup.get_document_title`;
 * :meth:`~markups.abstract.AbstractMarkup.get_javascript`;
 * :meth:`~markups.abstract.AbstractMarkup.get_stylesheet`.

Using the cache
===============

Markups are provided with :attr:`~markups.abstract.AbstractMarkup._cache`
dictionary that can contain any data shared between subsequent calls to
markup methods. Attribute :attr:`~markups.abstract._enable_cache`
indicates whether or not the cache should be used (set to ``False`` by
default).

For example, :meth:`~markups.abstract.AbstractMarkup.get_whole_html`
method sets :attr:`~markups.abstract._enable_cache` to ``True``, then
subsequently retrieves document title, body, javascript and stylesheet,
and sets :attr:`~markups.abstract._enable_cache` back to ``False``.
