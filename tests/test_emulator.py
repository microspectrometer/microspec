import unittest, os
from chromaspeclib.internal.emulator import *
from chromaspeclib.internal.data import *

class ChromaSpecTestEmulator(unittest.TestCase):

  def test_chromationEmulatorSettings(self):
    #TODO: when we make more settings, test them here
    e = ChromaSpecEmulator()

  def test_chromationEmulatorDefaults(self):
    e = ChromaSpecEmulator()
    self.test_chromationEmulatorCompare(e, e)

  def test_chromationEmulatorNull(self):
    e = ChromaSpecEmulator()
    assert e.process(CommandNull()) == []

  def test_chromationEmulatorVerify(self):
    e = ChromaSpecEmulator()
    assert e.process(CommandVerify()) == [SerialVerify(status=StatusOK)]

  def test_chromationEmulatorAutoExposure(self):
    e = ChromaSpecEmulator()
    assert e.process(CommandAutoExposure()) == \
                    [SerialAutoExposure(status=StatusOK),
                     SensorAutoExposure(status=StatusOK)]

  def test_chromationEmulatorCaptureFrame(self):
    e = ChromaSpecEmulator()
    #TODO: need to change this when we make the capture frame emulation better
    assert e.process(CommandCaptureFrame()) == \
                    [SerialCaptureFrame(status=StatusOK),
                     SensorCaptureFrame(status=StatusOK, num_pixels=4, pixels=[111,222,333,444])]

  def test_chromationEmulatorReset(self):
    e1 = ChromaSpecEmulator()
    e2 = ChromaSpecEmulator()
    self.test_chromationEmulatorSet(e2, bled0=LEDGreen, sled0=LEDRed, sled1=LEDGreen,
                                        binning=True, gain=Gain2_5x, rows=0x15, cycles=2345)
    assert e2.process(CommandReset()) == [SerialReset(status=StatusOK)]
    self.test_chromationEmulatorCompare(e2, e1)

  def test_chromationEmulatorCompare(self, emulator=None, control=None):
    #import pdb; pdb.set_trace()
    e = emulator or ChromaSpecEmulator()
    c = control  or emulator or ChromaSpecEmulator()
    assert e.process(CommandGetBridgeLED(led_num=0)) == \
                    [SerialGetBridgeLED(status=StatusOK, led_num=0, led_setting=c.bridge_led[0])]
    assert e.process(CommandGetSensorLED(led_num=0)) == \
                    [SerialGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusOK, led_num=0, led_setting=c.sensor_led[0])]
    assert e.process(CommandGetSensorLED(led_num=1)) == \
                    [SerialGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusOK, led_num=1, led_setting=c.sensor_led[1])]
    assert e.process(CommandGetSensorConfig()) == \
                    [SerialGetSensorConfig(status=StatusOK),
                     SensorGetSensorConfig(status=StatusOK, binning=c.binning, gain=c.gain, row_bitmap=c.rows)]
    assert e.process(CommandGetExposure()) == \
                    [SerialGetExposure(status=StatusOK),
                     SensorGetExposure(status=StatusOK, cycles=c.cycles)]

  def test_chromationEmulatorSet(self, emulator=None, bled0=LEDOff, sled0=LEDOff, sled1=LEDOff,
                                       binning=BinningDefault, gain=GainDefault, rows=RowsDefault, cycles=0):
    e = emulator or ChromaSpecEmulator()
    assert e.process(CommandSetBridgeLED(led_num=0, led_setting=bled0)) == \
                    [SerialSetBridgeLED(status=StatusOK)]
    assert e.process(CommandSetSensorLED(led_num=0, led_setting=sled0)) == \
                    [SerialSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusOK)]
    assert e.process(CommandSetSensorLED(led_num=1, led_setting=sled1)) == \
                    [SerialSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusOK)]
    assert e.process(CommandSetSensorConfig(binning=binning, gain=gain, row_bitmap=rows)) == \
                    [SerialSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusOK)]
    assert e.process(CommandSetExposure(cycles=cycles)) == \
                    [SerialSetExposure(status=StatusOK),
                     SensorSetExposure(status=StatusOK)]
    assert e.bridge_led[0] == bled0
    assert e.sensor_led[0] == sled0
    assert e.sensor_led[1] == sled1
    assert e.binning       == binning
    assert e.gain          == gain
    assert e.rows          == rows
    assert e.cycles        == cycles

  def test_chromationEmulatorBadData(self):
    e = ChromaSpecEmulator()
    assert e.process(CommandGetBridgeLED(led_num=-1)) == \
                    [SerialGetBridgeLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetBridgeLED(led_num=1)) == \
                    [SerialGetBridgeLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetSensorLED(led_num=-1)) == \
                    [SerialGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetSensorLED(led_num=2)) == \
                    [SerialGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandSetBridgeLED(led_num=-1, led_setting=LEDOff)) == \
                    [SerialSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetBridgeLED(led_num=1, led_setting=LEDOff)) == \
                    [SerialSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetBridgeLED(led_num=0, led_setting=99)) == \
                    [SerialSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=-1, led_setting=LEDOff)) == \
                    [SerialSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=2, led_setting=LEDOff)) == \
                    [SerialSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=2, led_setting=99)) == \
                    [SerialSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=-1, gain=GainDefault, row_bitmap=RowsDefault)) == \
                    [SerialSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=99, row_bitmap=RowsDefault)) == \
                    [SerialSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=GainDefault, row_bitmap=0x00)) == \
                    [SerialSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=GainDefault, row_bitmap=0x8000)) == \
                    [SerialSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetExposure(cycles=-1)) == \
                    [SerialSetExposure(status=StatusOK),
                     SensorSetExposure(status=StatusError)]
