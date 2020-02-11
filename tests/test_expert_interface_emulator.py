
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, sys
from timeit import default_timer as timer
from test_expert_interface import ChromaSpecTestExpertInterface
from chromaspeclib.expert  import ChromaSpecExpertInterface

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class ChromaSpecTestExpertInterfaceEmulator(ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.software = ChromaSpecExpertInterface(emulation=True, timeout=1)











