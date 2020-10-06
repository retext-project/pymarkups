==============
Custom Markups
==============

Registering the markup module
=============================

A third-party markup is a Python module that can be installed
the usual way.

To register your markup class with PyMarkups, make it inherit from
:class:`~markups.abstract.AbstractMarkup`, and add that class to
your module's ``entry_points``, in the “pymarkups” entry point group.

For example:

.. code-block:: python

   setup(
       ...
       entry_points={
           'pymarkups': [
               'mymarkup = mymodule:MyMarkupClass',
           ],
       },
       ...
   )

See the `setuptools documentation`_ on entry points for details.

To check if the module was found by Python-Markups, one can check
if the module is present in return value of
:func:`~markups.get_all_markups` function.

.. versionchanged:: 3.0
   The custom markups should be registered using the entry points
   mechanism, the ``pymarkups.txt`` file is no longer supported.

.. _`setuptools documentation`: https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html

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

