import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface           import _ChromaSpecTestExpertInterface
from chromaspeclib.expert            import ChromaSpecExpertInterface
from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.data     import *

from tabulate import tabulate

#@pytest.fixture
#def results(request):
#  session = request.node
#  return session.results

@pytest.mark.usefixtures("class_results")
class ChromaSpecTestExpertInterfaceEmulator(_ChromaSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.hardware = ChromaSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    self.software = ChromaSpecExpertInterface(device=self.hardware.software, timeout=1)

  def test_foo(self):
    self.results.append(["foo",20.24])

  def test_bar(self):
    self.results.append(["bar",22.22])

  def test_printResults(self):
    print()
    print(tabulate(self.results, headers='firstrow', tablefmt="pipe"))










