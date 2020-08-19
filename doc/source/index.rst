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

The important module
********************

The important module, from the application developer's perspective, is
``microspeclib.simple``. This is the *high-level* module that defines the main
class ``MicroSpecSimpleInterface``. Applications ``import`` this class to access
the API.

``MicroSpecSimpleInterface`` inherits from a *lower-level* class in
``microspeclib.expert``. Applications *never* need to access the *lower-level*
serial communication methods and attributes defined in ``microspeclib.expert``.

The documentation for ``microspeclib.simple`` is *the only documentation* of the
interface functions. There are no docstrings in the source code itself because
the ``microspeclib`` package *does not contain the dev-kit interface functions*.
All interface functions are auto-generated from the protocol defined in the JSON
file.

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

