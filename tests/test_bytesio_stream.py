import unittest, os, pytest
from io import BytesIO
from chromaspeclib.internal.stream import ChromationBytesIOStream

class ChromaspecTestBytesIOStream(unittest.TestCase):

  def test_defaultStream(self):
    b = BytesIO()
    s = ChromationBytesIOStream()
    assert b is not s.stream

  def test_parameterStream(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    assert b is s.stream

  def test_underlyingStreamRead1(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read(1)
    assert d[0] == r[0]
    assert len(r) == 1

  def test_underlyingStreamRead1Fail(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    d = b''
    b.write(d)
    r = s.read(1)
    assert len(r) == 0

  def test_underlyingStreamReadAll(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read()
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamReadManyFail(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read(10)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamWrite(self):
    b = BytesIO()
    s = ChromationBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    s.write(d)
    b.seek(0)
    w = b.read()
    assert     w  ==     d
    assert len(w) == len(d)

  def test_write1Read1(self):
    s = ChromationBytesIOStream()
    d = b'\x00'
    s.write(d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    # No consume() means no moving forwards
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_write1Read1Consume1(self):
    s = ChromationBytesIOStream()
    d = b'\x00'
    s.write(d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    s.consume(1)
    r = s.read(1)
    assert     r  ==     b''
    assert len(r) == len(b'')

  def test_writeManyRead1(self):
    s = ChromationBytesIOStream()
    d = b'\x00\x01\x02'
    s.write(d)
    r = s.read(1)
    assert     r  ==     d[0:1]
    assert len(r) == len(d[0:1])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[1:2]
    assert len(r) == len(d[1:2])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[2:3]
    assert len(r) == len(d[2:3])



















