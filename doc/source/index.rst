MicroSpec Documentation
=======================

Overview
--------

``microspec`` is Chromation's Spectrometer dev-kit interface. It contains:

- Python package :py:mod:`microspeclib <microspeclib.simple>`
    a collection of dev-kit interface functions

- command line utility :py:mod:`microspec-cmdline <bin.microspec_cmdline>`
    run basic measurements without developing a Python application

How the documentation is organized
----------------------------------

At the moment, this documentation is mostly *reference*. Tutorials and How-To
Guides are coming soon.

Getting Started
---------------

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

Detailed table of contents
--------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   how-to-read-this-documentation
   writing-applications
   Dev-kit API <microspeclib.simple>
   dev-kit-API-guide
   how-to-handle-timeouts
   under-the-hood
   microspec-dev

   modules

   bin

   cfg

   tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

