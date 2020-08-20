MicroSpec Dev
=============

Here is a short guide for contributing to ``microspec`` (or modifying for your
own purposes). Skip this section if you are only interested in writing
applications that use ``microspeclib``.

Setup
-----

Clone the repository:

.. code-block:: bash

   git clone https://github.com/microspectrometer/microspec.git

Install all the packages required for development:

.. code-block:: bash

  pip install microspec[dev]

To run tests using the hardware emulator, also install ``socat`` (Linux/Mac
only). If ``socat`` is not installed, ``pytest`` skips unit tests using the
emulator (so Windows users can still do most of the development work).

Workflow
^^^^^^^^

After modifying ``microspec``:

- run unit tests to check all tests still pass
- rebuild the documentation

Run tests
^^^^^^^^^

Run ``pytest`` at the root folder of the repository clone:

.. code-block:: bash

   cd microspec
   pytest

Rebuild documentation
^^^^^^^^^^^^^^^^^^^^^

Build the docs:

.. code-block:: bash

   cd microspec/doc
   make clean html

View the docs:

.. code-block:: bash

   cd microspec
   browse doc/build/html/index.html


