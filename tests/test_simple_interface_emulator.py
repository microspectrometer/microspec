
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, sys
from timeit import default_timer as timer
from test_simple_interface         import ChromaSpecTestSimpleInterface
from chromaspeclib.simple          import ChromaSpecSimpleInterface
from chromaspeclib.datatypes       import *

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class ChromaSpecTestSimpleInterfaceEmulator(ChromaSpecTestSimpleInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.software = ChromaSpecSimpleInterface(emulation=True, timeout=1)











