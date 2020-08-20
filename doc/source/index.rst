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

Applications typically configure the dev-kit in a **setup**, then
acquire spectra in a **loop**:

- setup:

  - set the *pixel configuration* in the spectrometer chip
  - set the *auto-expose parameters* in the dev-kit firmware

**The setup is optional**. The firmware powers-on with the recommended default
values.

- loop:

  - adjust **exposure time**, either *manually* or with *auto-expose*
  - acquire a **spectrum**
  - **save** and/or **plot** the spectrum

*The API only provides commands to control the dev-kit*. Data processing, such
as representing the data in a plot with a wavelength axis, is up to the
application.

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

The best way to read documentation is right here on *Read the Docs*. Jump
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

Under the hood
^^^^^^^^^^^^^^

Every API function call **sends a command** to the dev-kit and **receives a
reply** from the dev-kit.

All commands are sent (and replies received) via a single method,
``sendAndReceive()``. This method takes care of all low-level communication
concerns like waiting for a reply and packages the reply as an object with each
field in its own attribute.

For example, the reply to ``captureFrame()`` has attribute ``num_pixels`` (the
number of pixels in the frame) and attribute ``pixels`` (the actual pixel data).

Hardware under the hood
^^^^^^^^^^^^^^^^^^^^^^^

The dev-kit has a ``Sensor`` board that talks directly to the spectrometer chip
and a ``Bridge`` board that provides the USB interface to ``Sensor``. Most API
calls are commands for ``Sensor``. There are a few ``Bridge`` commands, but
applications do not need to use them.

Two APIs under the hood
^^^^^^^^^^^^^^^^^^^^^^^

``microspec`` actually has two APIs:

- ``microspeclib.simple``

  - *high-level* API for writing applications
  - hides the call to ``sendAndReceive()``
  - represents each command as its own API function calls, e.g.,
    ``setExposure(500)`` and ``reply=captureFrame()``

- ``microspeclib.expert``:

  - applications *never* need to use this API
  - this is a *low-level* API for troubleshooting communication
  - all commands are explicitly passed to ``sendAndReceive()``, e.g.,
    ``sendAndReceive(CommandSetExposure(cycles=500))`` and
    ``reply=sendAndReceive(CommandCaptureFrame())``
  - commands may also be *sent* and *received* separately, e.g.,
    ``sendCommand(CommandCaptureFrame())`` followed by ``reply=receiveReply()``

For an example of this lower-level interface, clone the ``microspec``
respository and see ``src/microspeclib/examples/microspec_lowlevel_api.py``

Where is the code?
^^^^^^^^^^^^^^^^^^

Do not look for the API function definitions in the source code. The
``microspeclib`` package *does not manually define dev-kit interface functions*.

The API function definitions are auto-generated by
``microspeclib.simple._generateFuction()`` using the protocol defined in JSON in
``microspec.cfg``.

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

