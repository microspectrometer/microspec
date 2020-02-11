#!/usr/bin/env python
from chromaspeclib.expert    import ChromaSpecExpertInterface
from chromaspeclib.datatypes import *

#xi = ChromaSpecExpertInterface(timeout=0.1)
#xi = ChromaSpecExpertInterface(timeout=0.1, device="COM3")
#xi = ChromaSpecExpertInterface(timeout=0.1, device="/dev/cu.usbserial-CHROMATION09310")
xi = ChromaSpecExpertInterface(timeout=0.1, emulation=True)

xi.sendCommand(CommandSetBridgeLED(led_num=0, led_setting=LEDOff))
print(xi.receiveReply())
xi.sendCommand(CommandSetSensorLED(led_num=0, led_setting=LEDGreen))
print(xi.receiveReply())
xi.sendCommand(CommandSetSensorLED(led_num=1, led_setting=LEDRed))
print(xi.receiveReply())

xi.sendCommand(CommandGetBridgeLED(led_num=0))
xi.sendCommand(CommandGetSensorLED(led_num=0))
xi.sendCommand(CommandGetSensorLED(led_num=1))
print(xi.receiveReply())
print(xi.receiveReply())
print(xi.receiveReply())

print(xi.sendAndReceive(CommandSetSensorConfig(binning=True, gain=Gain1x, row_bitmap=0x1F)))
print(xi.sendAndReceive(CommandSetExposure(cycles=100)))

import time
for i in range(0,5):
  print(xi.sendAndReceive(CommandCaptureFrame()))
  time.sleep(0.5)

