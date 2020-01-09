import unittest, os
from chromaspeclib.internal.emulator import *
from chromaspeclib.internal.data import *

class ChromaspecTestEmulator(unittest.TestCase):

  def test_chromationEmulatorSettings(self):
    #TODO: when we make more settings, test them here
    e = ChromationEmulator()

  def test_chromationEmulatorDefaults(self):
    e = ChromationEmulator()
    self.test_chromationEmulatorCompare(e, e)

  def test_chromationEmulatorCompare(self, emulator=None, control=None):
    #import pdb; pdb.set_trace()
    e = emulator or ChromationEmulator()
    c = control  or emulator or ChromationEmulator()
    assert e.process( CommandGetBridgeLED(led_num=0) ) == \
                    [ SerialGetBridgeLED( status=StatusOK, led_num=0, led_setting=c.bridge_led[0] ) ]
    assert e.process( CommandGetSensorLED(led_num=0) ) == \
                    [ SerialGetSensorLED( status=StatusOK ),
                      SensorGetSensorLED( status=StatusOK, led_num=0, led_setting=c.sensor_led[0] ) ]
    assert e.process( CommandGetSensorLED(led_num=1) ) == \
                    [ SerialGetSensorLED( status=StatusOK ),
                      SensorGetSensorLED( status=StatusOK, led_num=1, led_setting=c.sensor_led[1] ) ]
    assert e.process( CommandGetSensorConfig() ) == \
                    [ SerialGetSensorConfig( status=StatusOK ),
                      SensorGetSensorConfig( status=StatusOK, binning=c.binning, gain=c.gain, row_bitmap=c.rows ) ]
    assert e.process( CommandGetExposure() ) == \
                    [ SerialGetExposure( status=StatusOK ),
                      SensorGetExposure( status=StatusOK, cycles=c.cycles ) ]

