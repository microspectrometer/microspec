import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface           import ChromaSpecTestExpertInterface
from chromaspeclib.expert            import ChromaSpecExpertInterface
#from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
#from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

class ChromaSpecTestExpertInterfaceEmulator(ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.hardware = None
    self.software = ChromaSpecExpertInterface(timeout=0.1)












