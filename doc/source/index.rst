MicroSpec Documentation
=======================

Overview
********

``microspec`` is Chromation's Spectrometer dev-kit interface. It contains:

* Python package ``microspeclib``

    * a collection of dev-kit interface functions

* command line utility ``microspec-cmdline``

    * run basic measurements without developing a Python application

How the documentation is organized
**********************************

At the moment, this documentation is mostly *reference*. Tutorials and How-To
Guides are coming soon.

Until then, the easiest way to get started is to look at the example
applications in https://github.com/microspectrometer/dev-kit-2020.

Another good starting point for **writing applications** is to jump to the
:ref:`dev-kit-API-guide`.

And if you have the Chromation dev-kit, feel free to contact Chromation
directly:

* please email sara@chromationspec.com
* tell Sara:

  * what operating system you are using
  * what you'd like help with (e.g., a tutorial to get started, or a specific
    "how do I ...?")

Writing Applications
********************

``microspec`` contains many modules, but for writing applications, there is only
one module that matters: ``microspeclib.simple``.

``microspeclib.simple`` defines class ``MicroSpecSimpleInterface``.
*This class is the API.*

- create an instance of ``MicroSpecSimpleInterface`` to open communication with
  the dev-kit
- communication closes when the application exits, regardless of whether it
  exits normally or by an exception

Applications typically do some optional setup to configure the dev-kit, then
loop acquiring spectra:

- in the setup, set the spectrometer's pixel configuration and set the
  parameters used by auto-expose in the dev-kit firmware
- this setup is optional because the firmware powers-on with the recommended
  default values

- a typical loop:

  - adjusts exposure time, either manually or with auto-expose
  - acquires a spectrum
  - saves and/or plots the spectrum

Here is an example application that acquires a spectrum and exits:

.. code-block:: python

   # Access the API
   from microspeclib.simple import MicroSpecSimpleInterface

   # Open communication
   kit = MicroSpecSimpleInterface()

   # Set exposure time
   kit.setExposure(500) # 500 cycles * 20µs/cycle = 10ms exposure time

   # Acquire a spectrum
   frame = kit.captureFrame()

   # Guard against dropped frames (important if looping acquisition for hours)
   if frame is not None:
       counts = frame.pixels # the signal (in ADC counts) at each pixel

   # Do something with the spectrum
   print(counts)

   # Communication closes when this application exits.

Documentation
*************

The best way to read documentation is right here on *Read the Docs*. Searching
the source code fails because the API functions are auto-generated. Reading the
documentation with ``pydoc`` is not recommended because the docstrings are full
of *reStructuredText* markup for hyperlinks.

But if you are offline and did not download a copy of the docs from *Read the
Docs*, then ``pydoc`` is at least usable because the docstrings are formatted in
the NumPy style.

Read at the command line with pydoc:

.. code-block:: bash

   python -m pydoc microspeclib.simple._MicroSpecSimpleInterface

Or in a browser:

.. code-block:: bash

   python -m pydoc -b

Under the hood
^^^^^^^^^^^^^^

``MicroSpecSimpleInterface`` inherits from a *lower-level* class in
``microspeclib.expert``. Applications *never* need to access the *lower-level*
serial communication methods and attributes defined in ``microspeclib.expert``.

For an example of this lower-level interface, clone the ``microspec``
respository and see ``src/microspeclib/examples/microspec_lowlevel_api.py``

Do not look for the API function definitions in the source code. The
``microspeclib`` package *does not contain the dev-kit interface functions*. All
interface functions are auto-generated from the protocol defined in the JSON
file.

Developing microspec
********************

Setup
^^^^^

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

Detailed table of contents
**************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dev-kit-API-guide

   how-to-handle-timeouts

   modules

   bin

   cfg

   tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

