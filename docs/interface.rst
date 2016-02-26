================
Markup interface
================

The main class for interacting with markups is :class:`~markups.abstract.AbstractMarkup`.

However, you shouldn't create direct instances of that class. Instead, use one of the
:doc:`standard markup classes <standard_markups>`.

.. autoclass:: markups.abstract.AbstractMarkup
   :members:

When :class:`~markups.abstract.AbstractMarkup`'s
:meth:`~markups.abstract.AbstractMarkup.convert` method is called it will
return an instance of :class:`~markups.abstract.ConvertedMarkup` or a subclass
thereof that provides access to the conversion results.

.. autoclass:: markups.abstract.ConvertedMarkup
   :members:
