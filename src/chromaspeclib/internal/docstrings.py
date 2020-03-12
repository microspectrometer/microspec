
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

__doc__ = """Automated and static docstrings for json-generated classes, functions, and globals

Most of the API objects in ChromaSpecLib are dynamically generated from cfg/chromaspec.json.
For example CommandSetBridgeLED, ChromaSpecSimpleInterface.setBridgeLED, and LEDGreen are not
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
CommandSetBridgeLED and ChromaSpecSimpleInterface.setBridgeLED need the same documentation,
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
  "dt": "chromaspeclib.datatypes", 
  "led_status": """led_status: :data:`~{dt}.types.LEDOff`, :data:`~{dt}.types.LEDGreen`, or :data:`~{dt}.types.LEDRed`
                   The color state of the LED""",
  "status":     """status: :data:`~{dt}.types.StatusOK` or :data:`~{dt}.types.StatusError`
                   If there is an error status, the other attributes are not valid""",
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
:class:`~{dt}.bridge.BridgeGetBridgeLED`

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
led_num: 0-2
  The index of the LED on the Sensor

Returns
-------
:class:`~{dt}.bridge.BridgeGetSensorLED`
:class:`~{dt}.bridge.SensorGetSensorLED`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorLED"] = """Sets the current state of an LED on the Bridge board.

Parameters
----------
led_num: 0-2
  The index of the LED on the Sensor
{led_status}

Returns
-------
:class:`~{dt}.bridge.BridgeSetSensorLED`
:class:`~{dt}.bridge.SensorSetSensorLED`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandReset"] = """Resets the hardware and replies when the reset is complete.

Returns
-------
:class:`~{dt}.bridge.BridgeReset`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandVerify"] = """Verifies running status of the hardware.

Returns
-------
:class:`~{dt}.bridge.BridgeVerify`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetSensorConfig"] = """Retrieves the current sensor configuration.

Returns
-------
:class:`~{dt}.bridge.BridgeVerify`

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorConfig"] = ""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandAutoExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandCaptureFrame"] = ""

CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeNull"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetBridgeLED"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetBridgeLED"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorLED"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorLED"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeReset"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeVerify"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorConfig"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorConfig"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeAutoExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeCaptureFrame"] = ""

CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorLED"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorLED"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorConfig"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorConfig"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorAutoExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetExposure"] = ""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorCaptureFrame"] = ""

for protocol in CHROMASPEC_DYNAMIC_DOC:
  for klass in CHROMASPEC_DYNAMIC_DOC[protocol]:
    while [found for found in _common.keys() if "{%s}"%found in CHROMASPEC_DYNAMIC_DOC[protocol][klass]]:
      #import pdb; pdb.set_trace()
      CHROMASPEC_DYNAMIC_DOC[protocol][klass] = CHROMASPEC_DYNAMIC_DOC[protocol][klass].format(**_common)
