#!/usr/bin/env python
from chromaspeclib.simple    import ChromaSpecSimpleInterface
from chromaspeclib.datatypes import *

si = ChromaSpecSimpleInterface(timeout=0.1)
#si = ChromaSpecSimpleInterface(timeout=0.1, device="COM3")
#si = ChromaSpecSimpleInterface(timeout=0.1, device="/dev/cu.usbserial-CHROMATION09310")
#si = ChromaSpecSimpleInterface(timeout=0.1, emulation=True)

print(si.setBridgeLED(led_num=0, led_setting=LEDOff))
print(si.setSensorLED(led_num=0, led_setting=LEDGreen))
print(si.setSensorLED(led_num=1, led_setting=LEDRed))
print(si.getBridgeLED(led_num=0))
print(si.getSensorLED(led_num=0))
print(si.getSensorLED(led_num=1))

print(si.setSensorConfig(binning=True, gain=Gain1x, row_bitmap=0x1F))
print(si.setExposure(cycles=100))

import time
for i in range(0,5):
  print(si.captureFrame())
  time.sleep(0.5)

