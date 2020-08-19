
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

__doc__ = """Automated and static docstrings for json-generated classes, functions, and globals

Most of the API objects in MicroSpecLib are dynamically generated from cfg/microspec.json.
For example CommandSetBridgeLED, MicroSpecSimpleInterface.setBridgeLED, and LEDGreen are not
defined in code, they are created by meta-class factories, so that if the configuration changes
to permit new protocol commands and replies, the functions and classes will automatically update
as well. However, this causes a problem for documentation. 

Great pains were taken to auto-generate the proper function and class signatures such as
CommandSetBridgeLED(led_num=None, led_setting=None) rather than just CommandSetBridgeLED(\*args,
\**kwargs), so that pydoc and sphinx could introspect and document them properly. However,
the ONE thing that cannot be auto-generated is the per-function and per-class human-read
documentation. It could go into yet another json file and be auto-generated, but that would
be no more compact than making a file elsewhere for it. It could be written directly in
sphinx doc/source/\*.rst files, but then pydoc wouldn't find them. So the only choice left
is to make a separate internals docstrings library with the data in one place there, and
that is what this module is. Luckily, it at least saves some repetition, since both
CommandSetBridgeLED and MicroSpecSimpleInterface.setBridgeLED need the same documentation,
for example.

Thus, this module contains dictionaries for the different data and class types, and the datatype
module imports and implements them when it instantiates the metaclasses and generates the
globals. Since the json protocol and the documentation are separate, we must assume that one might
get out of sync with the other, thus it is assumed that this documentation may be missing
something. As such, implementers of these dictionaries should use DOC.get(value, None) and
handle lack of documentation in a responsible way.

The CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetBridgeLED"] contains that docstring, for example.

And the _common global is used to hold common replacement patterns, to eliminate having to type
the same things over and over below - they are replaced at the end of the module.

"""

CHROMASPEC_DYNAMIC_DOC = {"command":{}, "bridge":{}, "sensor":{}}

_common = { 
  "api": "microspeclib.simple.MicroSpecSimpleInterface",
  "dt": "microspeclib.datatypes", 
  "led_status": """led_status: :data:`~{dt}.types.LEDOff`, :data:`~{dt}.types.LEDGreen`, or :data:`~{dt}.types.LEDRed`""" + \
                """  The color state of the LED""",
  "status":     """status : :class:`MicroSpecInteger <microspeclib.internal.util.MicroSpecInteger>`"""
                """\n\n"""
                """  0: :data:`~{dt}.types.StatusOK`"""
                """\n"""
                """    The dev-kit successfully executed the command."""
                """\n\n"""
                """  1: :data:`~{dt}.types.StatusError`"""
                """\n"""
                """    The dev-kit failed to execute the command """
                """for one of the following reasons:"""
                """\n"""
                """\n      - serial communication failed"""
                """\n      - the command is invalid"""
                """\n      - one or more command parameters are invalid"""
                """\n\n"""
                """  If status is :data:`~{dt}.types.StatusError` """
                """the other attributes are not valid.""",
  "useful":     """see return values under **Parameters**""",
  "noimplement": """NOT IMPLEMENTED. Future: """,
  "notfinal":   """This is not the final payload for this command type. """  + \
                """If the Simple or Expert API returns this object, """ + \
                """then the command failed in the Bridge """ + \
                """and did not even make it to the Sensor.""",
  "null": """:py:func:`null <{api}.null>`""",
  "getBridgeLED": """:py:func:`getBridgeLED <{api}.getBridgeLED>`""",
  "setBridgeLED": """:py:func:`setBridgeLED <{api}.setBridgeLED>`""",
  "getSensorLED": """:py:func:`getSensorLED <{api}.getSensorLED>`""",
  "setSensorLED": """:py:func:`setSensorLED <{api}.setSensorLED>`""",
  "reset": """:py:func:`reset <{api}.reset>`""",
  "verify": """:py:func:`verify <{api}.verify>`""",
  "getSensorConfig": """:py:func:`getSensorConfig <{api}.getSensorConfig>`""",
  "setSensorConfig": """:py:func:`setSensorConfig <{api}.setSensorConfig>`""",
  "getExposure": """:py:func:`getExposure <{api}.getExposure>`""",
  "setExposure": """:py:func:`setExposure <{api}.setExposure>`""",
  "captureFrame": """:py:func:`captureFrame <{api}.captureFrame>`""",
  "autoExposure": """:py:func:`autoExposure <{api}.autoExposure>`""",
  "getAutoExposeConfig": """:py:func:`getAutoExposeConfig <{api}.getAutoExposeConfig>`""",
  "setAutoExposeConfig": """:py:func:`setAutoExposeConfig <{api}.setAutoExposeConfig>`""",
}

CHROMASPEC_DYNAMIC_DOC["command"]["CommandNull"] = """Null loopback request. The hardware will not reply,
but the API will still return a null reply object. This is primarily used to flush the line
in case of desynchronization.

Returns
-------
:class:`~{dt}.bridge.BridgeNull`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetBridgeLED"] = """Retrieves the current state of an LED on
the Bridge board.

Parameters
----------
led_num: 0
  The index of the LED on the Bridge

Returns
-------
:class:`~{dt}.bridge.BridgeGetBridgeLED` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetBridgeLED"] = """Sets the current state of an LED on the Bridge board.

Parameters
----------
led_num: 0
  The index of the LED on the Bridge
{led_status}

Returns
-------
:class:`~{dt}.bridge.BridgeSetBridgeLED`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetSensorLED"] = """Retrieves the current state of an LED on
the Sensor board.

Parameters
----------
led_num: 0, 1
  The index of the LED on the Sensor

Returns
-------
:class:`~{dt}.bridge.BridgeGetSensorLED`
:class:`~{dt}.sensor.SensorGetSensorLED` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorLED"] = """Sets the current state of an LED on the Bridge board.

Parameters
----------
led_num: 0, 1
  The index of the LED on the Sensor
{led_status}

Returns
-------
:class:`~{dt}.bridge.BridgeSetSensorLED`
:class:`~{dt}.sensor.SensorSetSensorLED` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandReset"] = """{noimplement} Resets the hardware and replies when the reset is complete.

Returns
-------
:class:`~{dt}.bridge.BridgeReset`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandVerify"] = """{noimplement} Verifies running status of the hardware.

Returns
-------
:class:`~{dt}.bridge.BridgeVerify`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetSensorConfig"] = """Retrieves the current sensor configuration.

Returns
-------
:class:`~{dt}.bridge.BridgeGetSensorConfig`
:class:`~{dt}.sensor.SensorGetSensorConfig` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorConfig"] = """Configure the
photodiode array in the spectrometer chip.

Parameters
----------
binning: 0 (off), 1 (on)
  with binning off there are 784 pixels with 7.8µm pitch, with binning on there
  are 392 pixels with 15.6µm pitch
gain: 0x01 (1x), 0x25 (2.5x), 0x04 (4x), 0x05 (5x)
  analog voltage gain applied to each pixel
row_bitmap:
  each pixel is 312.5µm tall and this height is divided into 5 sub-pixels
  which can be enabled/disabled.
  Activate all 5 with a binary bitmap of 5 1's, i.e. 0001 1111 or 0x1F.
  Any combination is permitted except 0x00.

Returns
-------
:class:`~{dt}.bridge.BridgeSetSensorConfig`
:class:`~{dt}.sensor.SensorSetSensorConfig` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandAutoExposure"] = """
Autoexpose the spectrometer: find the exposure time that results in the peak
signal in the configured pixel range to land in the configured target signal
range.

The autoexpose algorithm runs in the dev-kit firmware. Configure autoexpose
parameters with {setAutoExposeConfig}.

Returns success (0 or 1) and number of exposure times attempted.

Does not return the final exposure time. Get exposure time with
{getExposure}.

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> reply = kit.autoExposure()
>>> print(reply.success) # 1 means success
1
>>> print(reply.iterations) # number of exposure times before success/give-up
3

Returns
-------
:class:`~{dt}.bridge.BridgeAutoExposure`
:class:`~{dt}.sensor.SensorAutoExposure` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetAutoExposeConfig"] = """Retrieves the current auto-expose configuration.

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> reply = kit.getAutoExposeConfig()
>>> print(reply.max_tries)
12
>>> print(reply.start_pixel)
7
>>> print(reply.stop_pixel)
392
>>> print(reply.target)
46420
>>> print(reply.target_tolerance)
3277

Returns
-------
:class:`~{dt}.bridge.BridgeGetAutoExposeConfig`
:class:`~{dt}.sensor.SensorGetAutoExposeConfig` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetAutoExposeConfig"] = """Sets the current auto-expose configuration.

Parameters
----------
max_tries : int
    Maximum number of exposures to try before giving up.

    Valid range: 1-255

    If max_tries is 0:

        - reply status is ERROR
        - auto-expose configuration is not changed

    Dev-kit firmware defaults to `max_tries` = 10 on power-up.

    The auto-expose algorithm usually terminates after a couple
    of tries. Typically, therefore, the precise value of
    `max_tries` is not important.

    Adjusting `max_tries` is useful when troubleshooting why
    {autoExposure} fails. Also useful is the `iterations`
    parameter in :class:`~{dt}.sensor.SensorAutoExposure`.

start_pixel: 7-392 if binning on, 14-784 if binning off
  Auto-expose ignores pixels below start_pixel when checking if
  the peak is in the target range.

  Firmware defaults to 7 on power-up.
  Recommended value is the smallest pixel number in the
  pixel-to-wavelength map.

  If start_pixel is outside the allowed range, status is ERROR
  and the AutoExposeConfig is not changed.

stop_pixel: 7-392 if binning on, 14-784 if binning off, must be >= start_pixel
  Auto-expose ignores pixels above stop_pixel when checking if
  the peak is in the target range.

  Firmware defaults to 392 on power-up.
  Recommended value is the largest pixel number in the
  pixel-to-wavelength map.

  If stop_pixel < start_pixel, or if stop_pixel is outside the
  allowed range, status is ERROR and the AutoExposeConfig is not
  changed.

target: 4500-65535
  Target peak-counts for exposure gain calculation.

  Firmware defaults to 46420 counts on power-up.

  If target is outside the allowed range, status is ERROR and the
  AutoExposeConfig is not changed.

target_tolerance: 0-65535
  target +/- target_tolerance is the target peak-counts range.
  Auto-expose is finished when the peak counts lands in this
  range.

  Firmware defaults to 3277 counts on power-up.

  If the combination of target and target_tolerance results in
  target ranges extending below 4500 counts or above 65535
  counts, auto-expose ignores the target_tolerance and clamps the
  target range at these boundaries.

Returns
-------
:class:`~{dt}.bridge.BridgeSetAutoExposeConfig`
:class:`~{dt}.sensor.SensorSetAutoExposeConfig` ← {useful}

"""

CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetExposure"] = """Retrieve the current exposure setting, which may have been set
either by :class:`~{dt}.command.CommandSetExposure` or :class:`~{dt}.command.CommandAutoExposure`.

Returns
-------
:class:`~{dt}.bridge.BridgeGetExposure`
:class:`~{dt}.sensor.SensorGetExposure` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetExposure"] = """Set the exposure value for the sensor.

Parameters
----------
cycles: int
  Exposure time in cycles. Each cycle is 20µs. For example, a 1ms
  exposure time is 50 cycles.

  Valid range: 1-65535

Returns
-------
:class:`~{dt}.bridge.BridgeSetExposure`
:class:`~{dt}.sensor.SensorSetExposure` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandCaptureFrame"] = """Retrieve one set of captured pixels.

Returns
-------
:class:`~{dt}.bridge.BridgeCaptureFrame`
:class:`~{dt}.sensor.SensorCaptureFrame` ← {useful}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeNull"] = """This packet doesn't actually exist, as the request for a Null
has no reply. However, to distinguish between an error, when a :class:`~{dt}.command.CommandNull` is requested, the
API returns this object rather than None.

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetBridgeLED"] = """Contains the result of a :class:`~{dt}.command.CommandGetBridgeLED`
command.

Parameters
----------
{status}
led_num: 0
  Which LED the status applies to
{led_status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetBridgeLED"] = """Contains the status of the :class:`~{dt}.command.CommandSetBridgeLED`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorLED"] = """Contains a transitory status of the :class:`~{dt}.command.CommandGetSensorLED`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorLED"] = """Contains a transitory status of the :class:`~{dt}.command.CommandGetSensorLED`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeReset"] = """Contains status status of the :class:`~{dt}.command.CommandReset`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeVerify"] = """Contains the status of the :class:`~{dt}.command.CommandVerify`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorConfig"] = """Contains a transitory status of the :class:`~{dt}.command.CommandGetSensorConfig`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorConfig"] = """Contains a transitory status of the :class:`~{dt}.command.CommandSetSensorConfig`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeAutoExposure"] = """Contains a transitory status of the :class:`~{dt}.command.CommandAutoExposure`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetExposure"] = """Contains a transitory status of the :class:`~{dt}.command.CommandGetExposure`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetExposure"] = """Contains a transitory status of the :class:`~{dt}.command.CommandSetExposure`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeCaptureFrame"] = """Contains a transitory status of the :class:`~{dt}.command.CommandCaptureFrame`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""

CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorLED"] = """Contains the result of a :class:`~{dt}.command.CommandGetSensorLED`
command.

Parameters
----------
{status}
led_num: 0 or 1
  Which LED the status applies to
{led_status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorLED"] = """Contains the status of the :class:`~{dt}.command.CommandSetSensorLED`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorConfig"] = """Contains the result of a :class:`~{dt}.command.CommandGetSensorConfig`
command.

Parameters
----------
{status}
binning: 0, 1
  Whether or not to bin adjacent pixels.
  0: binning off, LIS-770i has 784 7.8µm-pitch pixels, 770 optically active
  1: binning on, LIS-770i has 392 15.6µm-pitch pixels, 385 optically active
gain: 0-255
  Analog pixel voltage gain. Allowed values:
  0x01: 1x gain
  0x25: 2.5x gain (37 in decimal)
  0x04: 4x gain
  0x05: 5x gain
row_bitmap:
  Which rows to permit sensing on. There are 5, and can all be
  activated with a binary bitmap of 5 1's, i.e. 011111 or 0x1F.
  The three most significant bits must be 0. Otherwise, any
  combination is permitted except 0x00.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorConfig"] = """Contains the result of a :class:`~{dt}.command.CommandSetSensorConfig`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorAutoExposure"] = """
Contains the result of the {autoExposure} command.

Parameters
----------
{status}

success : :class:`MicroSpecInteger <microspeclib.internal.util.MicroSpecInteger>`

  1: success
    Auto-expose settled on an exposure time that put the sensor
    peak value within the target range.

  0: failure
    Auto-expose gave up on finding an exposure time, either
    because it reached the maximum number of tries or the
    exposure time is already at the maximum allowed value.

iterations: 1-255

  Number of exposures tried by auto-expose.

  `iterations` never exceeds AutoExposeConfig parameter
  `max_tries`, as this sets the maximum number of iterations to
  try.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetExposure"] = """Contains the result of a :class:`~{dt}.command.CommandGetExposure`
command.

Parameters
----------
{status}
cycles: 1-65535
  Number of cycles to expose pixels. Each cycle is 20µs.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetExposure"] = """Contains the result of a :class:`~{dt}.command.CommandSetExposure`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorCaptureFrame"] = """Contains the result of a :class:`~{dt}.command.CommandCaptureFrame`
command.

Parameters
----------
{status}
num_pixels: 0-784
  The number of pixels to expect in the pixels parameter.
  Using the recommended (default) configuration, num_pixels is
  392.
pixels: Array of values, each from 0-65535
  The pixel values for one capture frame.

"""

for protocol in CHROMASPEC_DYNAMIC_DOC:
  for klass in CHROMASPEC_DYNAMIC_DOC[protocol]:
    while [found for found in _common.keys() if "{%s}"%found in CHROMASPEC_DYNAMIC_DOC[protocol][klass]]:
      #import pdb; pdb.set_trace()
      CHROMASPEC_DYNAMIC_DOC[protocol][klass] = CHROMASPEC_DYNAMIC_DOC[protocol][klass].format(**_common)
