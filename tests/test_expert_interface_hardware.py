
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface    import ChromaSpecTestExpertInterface
from chromaspeclib.expert     import ChromaSpecExpertInterface
from chromaspeclib.datatypes  import *
from chromaspeclib.exceptions import *

@pytest.mark.xfail(raises=ChromaSpecConnectionException, strict=False, reason="Hardware not connected")
class ChromaSpecTestExpertInterfaceHardware(ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = None
    if not hasattr(cls, "software"):
      cls.software = ChromaSpecExpertInterface(timeout=0.1)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    if hasattr(cls, "software"):
      del cls.software










