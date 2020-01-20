import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface           import _ChromaSpecTestExpertInterface
from chromaspeclib.expert            import ChromaSpecExpertInterface
from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

class ChromaSpecTestExpertInterfaceEmulator(_ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    import pdb; pdb.set_trace()
    self.hardware = ChromaSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    self.software = ChromaSpecExpertInterface(device=self.hardware.software, timeout=1)












