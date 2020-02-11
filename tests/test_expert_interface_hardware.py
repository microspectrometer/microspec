import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface           import ChromaSpecTestExpertInterface
from chromaspeclib.expert            import ChromaSpecExpertInterface
#from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
#from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

class ChromaSpecTestExpertInterfaceHardware(ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = None
    cls.software = ChromaSpecExpertInterface(timeout=0.1)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    del cls.software










