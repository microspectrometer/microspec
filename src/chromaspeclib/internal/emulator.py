from chromaspeclib.internal.data import *

class ChromationEmulator(object):
  
  def __init__(self):
    #TODO: more initialization state
    self.bridge_led = { 0: LEDOff }
    self.sensor_led = { 0: LEDOff, 1: LEDOff }
    self.binning    = BinningDefault
    self.gain       = GainDefault
    self.rows       = RowsDefault
    self.cycles     = 0 #TODO: default cycles value

  def process(self, command):
    if command.command_id == CommandGetBridgeLED.command_id:
      try:
        num = command.led_num
        assert 0 <= num <= 0
        return [ SerialReplyGetBridgeLED( led_num=num, led_setting=self.bridge_led[num], status=StatusOK ) ]
      except:
        return [ SerialReplyGetBridgeLED( led_num=num, led_setting=LEDOff,               status=StatusError ) ]
    elif command.command_id == CommandSetBridgeLED.command_id:
      try:
        num = command.led_num
        led = command.led_setting
        assert 0 <= num <= 0
        assert led in [ LEDOff, LEDGreen, LEDRed ]
        self.bridge_led[num] = led
        return [ SerialReplySetBridgeLED( status=StatusOK ) ]
      except:
        return [ SerialReplySetBridgeLED( status=StatusError ) ]
    elif command.command_id == CommandGetSensorLED.command_id:
      try:
        num = command.led_num
        assert 0 <= num <= 1
        return [ SerialReplyGetSensorLED(                                                status=StatusOK ),
                 SensorReplyGetSensorLED( led_num=num, led_setting=self.serial_led[num], status=StatusOK ) ]
      except:
        return [ SerialReplyGetSensorLED(                                                status=StatusOK ),
                 SensorReplyGetSensorLED( led_num=num, led_setting=LEDOff,               status=StatusError ) ]
    elif command.command_id == CommandSetSensorLED.command_id:
      try:
        num = command.led_num
        led = command.led_setting
        assert 0 <= num <= 1
        assert led in [ LEDOff, LEDGreen, LEDRed ]
        self.bridge_led[num] = led
        return [ SerialReplySetSensorLED( status=StatusOK ),
                 SensorReplySetSensorLED( status=StatusOK ) ]
      except:
        return [ SerialReplySetSensorLED( status=StatusOK ),
                 SensorReplySetSensorLED( status=StatusError ) ]
    elif command.command_id == CommandReset.command_id:
        return [ SerialReplyReset( status=StatusOK ) ]
    elif command.command_id == CommandVerify.command_id:
        return [ SerialReplyVerify( status=StatusOK ) ]
    elif command.command_id == CommandNull.command_id:
      return []
    elif command.command_id == CommandGetSensorConfig.command_id:
      return [ SerialReplyGetSensorConfig( status=StatusOK ),
               SensorReplyGetSensorConfig( status=StatusOK, binning=self.binning, gain=self.gain, row_bitmap=self.rows ) ]
    elif command.command_id == CommandGetSensorConfig.command_id:
      try:
        assert False <= command.binning <= True
        assert command.gain in [ Gain1x, Gain2_5x, Gain4x, Gain5x ]
        assert command.row_bitmap != 0
        assert command.row_bitmap&0x1F != 0
        self.gain = gain
        self.binning = command.binning
        self.rows = command.row_bitmap
        return [ SerialReplySetSensorLED( status=StatusOK ),
                 SensorReplySetSensorLED( status=StatusOK ) ]
      except:
        return [ SerialReplySetSensorConfig( status=StatusOK ),
                 SensorReplySetSensorConfig( status=StatusError ) ]
    elif command.command_id == CommandAutoExposure.command_id:
      return [ SerialReplyAutoExposure( status=StatusOK ),
               SensorReplyAutoExposure( status=StatusOK ) ]
    elif command.command_id == CommandGetExposure.command_id:
      return [ SerialReplyGetExposure( status=StatusOK ),
               SensorReplyGetExposure( status=StatusOK, cycles=self.cycles ) ]
    elif command.command_id == CommandSetExposure.command_id:
      try:
        assert 0x00 <= command.cycles <= 0xFFFF
        self.cycles = command.cycles
        return [ SerialReplySetExposure( status=StatusOK ),
                 SensorReplySetExposure( status=StatusOK ) ]
      except:
        return [ SerialReplySetExposure( status=StatusOK ),
                 SensorReplySetExposure( status=StatusError ) ]
    elif command.command_id == CommandCaptureFrame.command_id:
      #TODO: big todo - play back recorded or make up data etc
      return [ SerialReplyCaptureFrame( status=StatusOK ),
               SensorReplyCaptureFrame( status=StatusOK, num_pixels=4, pixels=[111,222,333,444] ) ]
    
