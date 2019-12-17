import unittest, os
from chromaspeclib.internal.util import ChromationInteger, isInt, dehex

class ChromaspecTestUtil(unittest.TestCase):

  def test_chromationInteger(self):
    ints = [ 
      [    0, 1,    "big", False,     b'\x00' ],
      [    1, 1,    "big", False,     b'\x01' ],
      [    1, 2,    "big", False, b'\x00\x01' ],
      [    1, 2, "little", False, b'\x01\x00' ],
      [ -128, 1,    "big",  True,     b'\x80' ],
      [  127, 1,    "big",  True,     b'\x7f' ],
      [   -1, 1,    "big",  True,     b'\xff' ],
      [  255, 1,    "big", False,     b'\xff' ],
    ]
    for i in ints:
      ci = ChromationInteger( i[0], i[1], i[2], i[3] )
      assert ci == i[0]
      b = bytes(ci)
      assert b == i[4]
    
  def test_isInt(self):
    assert isInt(1)     == True
    assert isInt("1")   == False
    assert isInt(None)  == False
    #assert isInt(False) == False # These actually turn out to be True
    #assert isInt(True)  == False # These actually turn out to be True

  def test_dehex(self):
    assert dehex("FF")   == "FF"
    assert dehex("1")    == "1"
    assert dehex("0xFF") == 255
    assert dehex("0xff") == 255

