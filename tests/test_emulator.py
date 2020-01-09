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

  def test_chromationEmulatorNull(self):
    e = ChromationEmulator()
    assert e.process( CommandNull() ) == []

  def test_chromationEmulatorVerify(self):
    e = ChromationEmulator()
    assert e.process( CommandVerify() ) == [ SerialVerify( status=StatusOK ) ]

  def test_chromationEmulatorAutoExposure(self):
    e = ChromationEmulator()
    assert e.process( CommandAutoExposure() ) == \
                    [ SerialAutoExposure( status=StatusOK ),
                      SensorAutoExposure( status=StatusOK ) ]

  def test_chromationEmulatorCaptureFrame(self):
    e = ChromationEmulator()
    #TODO: need to change this when we make the capture frame emulation better
    assert e.process( CommandCaptureFrame() ) == \
                    [ SerialCaptureFrame( status=StatusOK ),
                      SensorCaptureFrame( status=StatusOK, num_pixels=4, pixels=[111,222,333,444] ) ]

  def test_chromationEmulatorReset(self):
    e1 = ChromationEmulator()
    e2 = ChromationEmulator()
    self.test_chromationEmulatorSet(e2, bled0=LEDGreen, sled0=LEDRed, sled1=LEDGreen,
                                        binning=True, gain=Gain2_5x, rows=0x15, cycles=2345)
    assert e2.process( CommandReset() ) == [ SerialReset(status=StatusOK) ]
    self.test_chromationEmulatorCompare(e2, e1)

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

  def test_chromationEmulatorSet(self, emulator=None, bled0=LEDOff, sled0=LEDOff, sled1=LEDOff,
                                       binning=BinningDefault, gain=GainDefault, rows=RowsDefault, cycles=0):
    e = emulator or ChromationEmulator()
    assert e.process( CommandSetBridgeLED( led_num=0, led_setting=bled0 ) ) == \
                    [ SerialSetBridgeLED( status=StatusOK ) ]
    assert e.process( CommandSetSensorLED( led_num=0, led_setting=sled0 ) ) == \
                    [ SerialSetSensorLED( status=StatusOK ),
                      SensorSetSensorLED( status=StatusOK ) ]
    assert e.process( CommandSetSensorLED( led_num=1, led_setting=sled1 ) ) == \
                    [ SerialSetSensorLED( status=StatusOK ),
                      SensorSetSensorLED( status=StatusOK ) ]
    assert e.process( CommandSetSensorConfig( binning=binning, gain=gain, row_bitmap=rows ) ) == \
                    [ SerialSetSensorConfig( status=StatusOK ),
                      SensorSetSensorConfig( status=StatusOK ) ]
    assert e.process( CommandSetExposure( cycles=cycles ) ) == \
                    [ SerialSetExposure( status=StatusOK ),
                      SensorSetExposure( status=StatusOK ) ]
    assert e.bridge_led[0] == bled0
    assert e.sensor_led[0] == sled0
    assert e.sensor_led[1] == sled1
    assert e.binning       == binning
    assert e.gain          == gain
    assert e.rows          == rows
    assert e.cycles        == cycles

