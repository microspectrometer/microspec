How To Read This Documentation
==============================

The best way to read the documentation is right here on *Read the Docs*. Jump
straight to the :ref:`dev-kit-API-guide`.

Searching the source code fails because the API functions are auto-generated.
Reading the documentation with ``pydoc`` is not recommended because the
docstrings are full of *reStructuredText* markup for hyperlinks.

But if you are offline and did not download a copy of the docs from *Read the
Docs*, then ``pydoc`` is at least usable because the docstrings are formatted in
the NumPy style.

Read at the command line with pydoc:

.. code-block:: bash

   python -m pydoc microspeclib.simple._MicroSpecSimpleInterface

Or in a browser:

.. code-block:: bash

   python -m pydoc -b


