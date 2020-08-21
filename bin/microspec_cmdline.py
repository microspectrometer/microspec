#!/usr/bin/env python

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

"""
=============
Example Usage
=============

--------
Get help
--------
::

    $ microspec-cmdline -h
    usage: cmdline.py [-h] [-d] [-v] [-t TIMEOUT] [-r REPEAT] [-w WAIT] [-e]
                      [-f FILE] [-c]
                      command [arguments [arguments ...]]

    Command line interface for MicroSpecLib

    positional arguments:
      command               Command to send
      arguments             Key=value pairs for command

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Internal debugging trace
      -v, --verbose         Verbose trace
      -t TIMEOUT, --timeout TIMEOUT
                            Timeout (seconds)
      -r REPEAT, --repeat REPEAT
                            Repeat N times, 1=once, 0=forever
      -w WAIT, --wait WAIT  Wait inbetween repeats (seconds)
      -e, --emulator        Spawn emulator and connect to that
      -f FILE, --file FILE  File/socket/device to connect to, default=auto-detect
                            hardware
      -c, --csv             Print-format: 'default' or 'csv'

    List of commands and arguments:
      Null              
      GetBridgeLED      led_num=xxx
      SetBridgeLED      led_num=xxx led_setting=xxx
      GetSensorLED      led_num=xxx
      SetSensorLED      led_num=xxx led_setting=xxx
      Reset             
      Verify            
      GetSensorConfig   
      SetSensorConfig   binning=xxx gain=xxx row_bitmap=xxx
      GetExposure       
      SetExposure       cycles=xxx
      CaptureFrame      
      AutoExposure      
      GetAutoExposeConfig 
      SetAutoExposeConfig max_tries=xxx start_pixel=xxx stop_pixel=xxx
                          target=xxx target_tolerance=xxx max_exposure=xxx


--------------------
Blink the debug LEDs
--------------------

Turn Bridge LED red
^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline setbridgeled led_num=0 led_setting=2
    2020-08-20T22:08:46.530318,BridgeSetBridgeLED(status=0)

Turn one Sensor LED red
^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline setsensorled led_num=1 led_setting=2
    2020-08-20T22:11:42.458425,SensorSetSensorLED(status=0)

*Try* to turn the other Sensor LED red... it stays green
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline setsensorled led_num=0 led_setting=2
    2020-08-20T22:13:01.087770,SensorSetSensorLED(status=0)

Notes
-----
    Sensor ``led0`` indicates when the Sensor microcontoller is
    busy.

    - ``led0`` is **red** while **busy** executing a command
    - ``led0`` is **green** when execution is **done**

------------
Measurements
------------

Capture one frame once
^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline captureframe
    2020-08-20T22:29:37.850778,SensorCaptureFrame(status=0,
    num_pixels=392, pixels=[7912, 7306, 7303, 7282, ..., 0])

Capture a frame 50 times with 2 seconds inbetween
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline captureframe -r 50 -w 2
    $ microspec-cmdline captureframe -r 2 -w 2
    2020-08-20T22:37:26.765253,SensorCaptureFrame(status=0,
    num_pixels=392, pixels=[7888, 7461, 7376, 7388, ..., 0])
    ...
    2020-08-20T22:39:06.809406,SensorCaptureFrame(status=0,
    num_pixels=392, pixels=[7848, 7657, 7526, 7238, ..., 0])

Capture a frame and print results in csv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline captureframe -c
    2020-08-20T22:35:21.376177,SensorCaptureFrame,status,0,
    num_pixels,392,pixels,7898,7518,7172,7435,7847,7768,...,0

-----------------------------
Configure spectrometer pixels
-----------------------------

pixel binning ON, pixel gain 1x, all rows on (full pixel height)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline setsensorconfig binning=1 gain=1 row_bitmap=0x1F
    2020-08-20T22:45:38.043012,SensorSetSensorConfig(status=0)

----------------
Specify USB port
----------------

Connect to a specific port on Linux/Mac
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline -f /dev/ttyUSB0 setbridgeled led_num=0 led_setting=1
    2020-08-20T22:50:49.633144,BridgeSetBridgeLED(status=0)

Connect to a specific COM port on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline -f COM4 setbridgeled led_num=0 led_setting=1


Connect to emulator instead of hardware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ microspec-cmdline -e captureframe
    2020-08-21T01:20:12.985962,SensorCaptureFrame(status=0,
    num_pixels=4, pixels=[111, 222, 333, 444])

"""

def main():
  import subprocess, sys
  subprocess.call(["python", "-m", "microspeclib.cmdline"] + sys.argv[1:])
  
if __name__ == "__main__":
  main()
