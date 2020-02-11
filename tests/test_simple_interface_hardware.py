import unittest, os, pytest
from timeit import default_timer as timer
from test_simple_interface           import ChromaSpecTestSimpleInterface
from chromaspeclib.simple            import ChromaSpecSimpleInterface
from chromaspeclib.internal.data     import *

class ChromaSpecTestSimpleInterfaceHardware(ChromaSpecTestSimpleInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = None
    cls.software = ChromaSpecSimpleInterface(timeout=0.1)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    del cls.software











