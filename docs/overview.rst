============
API overview
============

For the basic usage of Python-Markups, one should import some markup
class from :mod:`markups`, create an instance of that class, and use
the :meth:`~markups.abstract.AbstractMarkup.convert` method:

>>> import markups
>>> markup = markups.ReStructuredTextMarkup()
>>> markup.convert('*reStructuredText* test').get_document_body()
'<div class="document">\n<p><em>reStructuredText</em> test</p>\n</div>\n'

For advanced usage (like dynamically choosing the markup class),
one may use one of the functions documented below.

Getting lists of available markups
==================================

.. autofunction:: markups.get_all_markups
.. autofunction:: markups.get_available_markups

Getting a specific markup
=========================

.. autofunction:: markups.get_markup_for_file_name
.. autofunction:: markups.find_markup_class_by_name

.. _configuration-directory:

Configuration directory
=======================

Some markups can provide configuration files that the user may use
to change the behavior.

These files are stored in a single configuration directory.

If :envvar:`XDG_CONFIG_HOME` is defined, then the configuration
directory is it. Otherwise, it is :file:`.config` subdirectory in
the user's home directory.
