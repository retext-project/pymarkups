==============
Custom Markups
==============

Registering the markup module
=============================

A third-party markup is a Python module that can be installed
the usual way.
Every module should have :data:`markup` property pointing to
the markup class.

To register the markup, one should append the full module name to
file named ``pymarkups.txt`` in the
:ref:`configuration directory <configuration-directory>`.

To check if the module was found by Python-Markups, one can check
if the module is present in return value of
:func:`~markups.get_custom_markups` function.

.. versionchanged:: 0.6
   The third-party markup is now a normal Python module, not
   necessarily a file in ``markups`` namespace.

Importing third-party modules
=============================

A markup must not directly import any third party Python module it uses
at file level. Instead, it should check the module availability in
:meth:`~markups.abstract.AbstractMarkup.available` static method.

That method can try to import the needed modules, and return ``True`` in
case of success, and ``False`` in case of failure.

Implementing methods
====================

Any markup must inherit from :class:`~markups.abstract.AbstractMarkup`.

Third-party markups must implement :class:`~markups.abstract.AbstractMarkup`'s
:meth:`~markups.abstract.AbstractMarkup.convert` method, which must perform the
time-consuming part of markup conversion and return a newly constructed
instance of (a subclass of) :class:`~markups.abstract.ConvertedMarkup`.

:class:`~markups.abstract.ConvertedMarkup` encapsulates the title, body,
stylesheet and javascript of a converted document. Of these only the body is
required during construction, the others default to an empty string.  If
additional markup-specific state is required to implement
:class:`~markups.abstract.ConvertedMarkup`, a subclass can be defined and an
instance of it returned from :meth:`~markups.abstract.AbstractMarkup.convert`
instead.

