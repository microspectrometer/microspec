microspeclib.simple module
===========================

Return values
*************

.. note::

   The ``Returns`` section for each command only lists the datatypes, not the
   return values.

   **Click the ``Sensor`` datatype link to view the documented
   return values.**

Another way to find out what a command returns is by printing its reply:

* open a Python REPL
* send the command
* print its reply

Example:

.. code-block:: python
   :emphasize-lines: 4

   from microspeclib.simple import MicroSpecSimpleInterface
   kit = MicroSpecSimpleInterface(timeout=2.0)
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

.. automodule:: microspeclib.simple
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: consume, flush, pushback, read, receiveCommand, receiveReply, sendAndReceive, sendCommand, sendReply, write
