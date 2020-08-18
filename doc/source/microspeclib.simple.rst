dev-kit API (microspeclib.simple module)
========================================

This is the most important page in the documentation. Every command in the API
is documented here.

The documentation for *the values* returned by each command is somewhere else,
but the links to that documentation are here.

Return values
*************

.. note::

   In the ``Returns`` section for each command, click the ``Sensor`` datatype
   link to view the documented return values.

Another way to find out what a command returns is by printing its reply:

* open a Python REPL
* send the command
* print its reply

Example:

.. code-block:: python
   :emphasize-lines: 4

   from microspeclib.simple import MicroSpecSimpleInterface
   kit = MicroSpecSimpleInterface()
   reply = kit.autoExposure()
   print(reply)

Reply:

.. code-block::

   SensorAutoExposure(status=0, success=0, iterations=1)

The values are accessed as ``reply.success``, ``reply.iterations``, etc.

*Every* command reply includes ``status``.

``status`` is part of the *low-level* serial communication data and is safe to
ignore as an API user. For example, Chromation's ``microspecgui`` application
never checks the reply status.

The default timeout is 2 seconds, but sometimes a command will timeout. If a
command timeouts, the reply is ``None``.

The most likely scenario to encounter a timeout is when acquiring spectra in a
loop. For example, Chromation's ``microspecgui`` is constantly acquiring frames
of spectrum data:

.. code-block:: python

   frame = kit.captureFrame() # acquire a spectrum
   counts = frame.pixels # the signal (in ADC counts) at each pixel

If this application runs for several hours, it is likely to drop a frame at
least once. When that happens ``frame`` is ``None``, raising the Exception:
``NoneType`` has no attribute ``pixels``.

A single dropped frame is not a reason to exit the application. Instead of
quitting, ignore the dropped frame and use the previous value stored in
``counts``:

.. code-block:: python

   frame = kit.captureFrame()
   if frame is not None: counts = frame.pixels


.. automodule:: microspeclib.simple
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: consume, flush, pushback, read, receiveCommand, receiveReply, sendAndReceive, sendCommand, sendReply, write
