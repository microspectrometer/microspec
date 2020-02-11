import unittest, os, pytest, sys
from timeit import default_timer as timer
from test_expert_interface           import ChromaSpecTestExpertInterface
from chromaspeclib.expert            import ChromaSpecExpertInterface
from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

from tabulate import tabulate

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class ChromaSpecTestExpertInterfaceEmulator(ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = ChromaSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    cls.software = ChromaSpecExpertInterface(device=cls.hardware.software, timeout=1)











