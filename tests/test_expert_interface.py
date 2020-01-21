import unittest, os, pytest, time
from timeit import default_timer as timer
from chromaspeclib.expert            import ChromaSpecExpertInterface
from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

# Abstract class that emulator and hardware inherit from, thus the _Test name, so it won't run
class _ChromaSpecTestExpertInterface(unittest.TestCase):
  __test__ = False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.hardware = None
    self.software = None
    self.emulator = ChromaSpecEmulator()
    self.min      = 0

  def test_minimalProcessing(self):
    for i in range(0,100):
      t1 = timer()    
      self.software.sendCommand(CommandGetBridgeLED(led_num=255))
      r  = self.software.receiveReply()
      t2 = timer()    
      assert r == SerialGetBridgeLED(status=1, led_setting=0)
      self.min += t2 - t1
    self.min /= 100
    










