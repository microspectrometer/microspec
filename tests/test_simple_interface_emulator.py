import unittest, os, pytest, sys
from timeit import default_timer as timer
from test_simple_interface           import ChromaSpecTestSimpleInterface
from chromaspeclib.simple            import ChromaSpecSimpleInterface
from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

from tabulate import tabulate

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class ChromaSpecTestSimpleInterfaceEmulator(ChromaSpecTestSimpleInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = ChromaSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    cls.software = ChromaSpecSimpleInterface(device=cls.hardware.software, timeout=1)











