import unittest, os, pytest, time
from timeit import default_timer as timer
from tabulate import tabulate
from chromaspeclib.expert                import ChromaSpecExpertInterface
from chromaspeclib.internal.emulator     import ChromaSpecEmulator
from chromaspeclib.internal.data         import *
from chromaspeclib.internal.data.command import CHROMASPEC_COMMAND_ID

@pytest.mark.usefixtures("class_results")
class ChromaSpecTestExpertInterface(unittest.TestCase):
  __test__ = False # Abstract test class #

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.hardware = None
    self.software = None
    self.emulator = ChromaSpecEmulator()
    self.min      = 0

  @classmethod
  def setUpClass(cls):
    cls.setup = False

  def setUp(self):
    if self.__class__.setup:
      return
    command = CommandGetBridgeLED(led_num=255)
    for i in range(0,100):
      t1 = timer()    
      self.software.sendCommand(command)
      r  = self.software.receiveReply()
      t2 = timer()    
      assert r == SerialGetBridgeLED(status=1, led_setting=0)
      self.min += t2 - t1
    self.min /= 100
    self.results.append([command.__class__.__name__ + "(Reference)", self.min*1000])
    self.__class__.setup = True

  @classmethod
  def tearDownClass(self):
    print()
    print(tabulate(self.results, headers='firstrow', tablefmt="pipe"))

def generateTest(command_class):
  def test(self):
    command = command_class()
    if command_class is CommandSetSensorConfig:
      command.binning    = True
      command.gain       = Gain1x
      command.row_bitmap = 0x1F
    elif command_class is CommandSetExposure:
      command.cycles  = 1
    else:
      for var in command:
        command[var]  = 0
    replies = self.emulator.process(command)
    if replies:
      expected_reply = replies.pop()
    else:
      expected_reply = SerialNull()
    avg = 0
    for i in range(0,100):
      t1 = timer()    
      self.software.sendCommand(command)
      r  = self.software.receiveReply()
      t2 = timer()    
      assert r == expected_reply
      avg += t2 - t1
    avg /= 100
    avg -= self.min
    self.results.append([command.__class__.__name__, avg*1000])
  return test

for command_id, command_class in CHROMASPEC_COMMAND_ID.items():
  if command_id < 0:
    continue
  setattr(ChromaSpecTestExpertInterface, "test_sending"+command_class.__name__, generateTest(command_class))

