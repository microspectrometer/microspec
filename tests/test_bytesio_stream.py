import unittest, os, pytest
from io import BytesIO
from chromaspeclib.internal.stream       import ChromaSpecBytesIOStream
from chromaspeclib.internal.data         import *
from chromaspeclib.internal.data.command import CHROMASPEC_COMMAND_ID

#from chromaspeclib.internal.logger import CHROMASPEC_LOGGER_STREAM
#import logging
#CHROMASPEC_LOGGER_STREAM.setLevel(logging.DEBUG)

class ChromaSpecTestBytesIOStream(unittest.TestCase):

  def generate_streams(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    return b, s

  def test_defaultStream(self):
    b, s = self.generate_streams()
    s = ChromaSpecBytesIOStream()
    assert b is not s.stream

  def test_parameterStream(self):
    b, s = self.generate_streams()
    assert b is s.stream

  def test_underlyingStreamRead1(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(1)
    assert d[0] == r[0]
    assert len(r) == 1

  def test_underlyingStreamRead1Fail(self):
    b, s = self.generate_streams()
    d = b''
    self.write_underlying(b, s, d)
    r = s.read(1)
    assert len(r) == 0

  def test_underlyingStreamReadAll(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(3)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamReadManyFail(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(10)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamWrite(self):
    b, s = self.generate_streams()
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    self.write_direct(b, s, d)
    self.seek( s, 0 )
    w = s.read()
    assert     w  ==     d
    assert len(w) == len(d)

  def test_write1Read1(self):
    b, s = self.generate_streams()
    d = b'\x00'
    self.write_direct(b, s, d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    # No consume() means no moving forwards
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_write1Read1Consume1(self):
    b, s = self.generate_streams()
    d = b'\x00'
    self.write_direct(b, s, d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    s.consume(1)
    r = s.read(1)
    assert     r  ==     b''
    assert len(r) == len(b'')

  def test_writeManyRead1(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_direct(b, s, d)
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

  def test_writeManyReadInterleaved(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02\x03\x04\x05'
    self.write_direct(b, s, d[0:3])
    r = s.read(1)
    assert     r  ==     d[0:1]
    assert len(r) == len(d[0:1])
    self.write_direct(b, s, d[3:4])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[1:2]
    assert len(r) == len(d[1:2])
    s.consume(1)
    self.write_direct(b, s, d[4:5])
    r = s.read(1)
    assert     r  ==     d[2:3]
    assert len(r) == len(d[2:3])
    s.consume(1)
    r = s.read(1)
    self.write_direct(b, s, d[5:6])
    assert     r  ==     d[3:4]
    assert len(r) == len(d[3:4])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[4:5]
    assert len(r) == len(d[4:5])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[5:6]
    assert len(r) == len(d[5:6])

  def test_writeManyReadPartialConsume(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02\x03\x04\x05'
    self.write_direct(b, s, d)
    r = s.read(4)
    assert     r  ==     d[0:4]
    assert len(r) == len(d[0:4])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[2:6]
    assert len(r) == len(d[2:6])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[4:6]
    assert len(r) == len(d[4:6])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[6:6]
    assert len(r) == len(d[6:6])

  def test_writeReadCommand(self):
    b, s = self.generate_streams()
    w = []
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      cklass = getCommandByID(cid)
      c      = cklass()
      for v in c:
        c[v] = 99 # dummy data
      c.command_id = cklass.command_id # varibles include this, need to undo it
      self.sendCommand(b, s, c)
      w.append(c)
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      c1 = s.receiveCommand()
      c2 = w.pop(0)
      assert c1 == c2

  def test_partialReadCommand(self):
    b, s = self.generate_streams()
    c = CommandGetBridgeLED(led_num=0)
    self.assert_getvalue(s.stream, b'')

    cb = bytes(c)
    cb1 = cb[0:len(cb)-1]
    cb2 = cb[len(cb)-1:]
    self.write_direct(b, s, cb1)
    self.assert_getvalue(s.stream, cb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    r = s.receiveCommand()
    self.assert_getvalue(s.stream, cb1)
    self.assert_readpos( s,        1  )
    assert s.buffer            == cb1
    assert r is None

    s.write(cb2)
    self.assert_getvalue(s.stream, cb1+cb2)
    self.assert_readpos( s,        1      )
    assert s.buffer            == cb1

    r = s.receiveCommand()
    self.assert_getvalue(s.stream, cb1+cb2)
    self.assert_readpos( s,        2      )
    assert s.buffer            == b''
    assert r == CommandGetBridgeLED(led_num=0)

  def test_partialReadSerialReply(self):
    b, s = self.generate_streams()
    r = SerialGetBridgeLED(status=0, led_num=0, led_setting=1)
    self.assert_getvalue(s.stream, b'')

    rb = bytes(r)
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    x = s.receiveReply(r.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        1  )
    assert s.buffer            == rb1
    assert x is None

    s.write(rb2)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        1      )
    assert s.buffer            == rb1

    x = s.receiveReply(r.command_id)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        2      )
    assert s.buffer            == b''
    assert x == SerialGetBridgeLED(status=0, led_num=0, led_setting=1)

  def test_partialReadSerialAndSensorReply(self):
    b, s = self.generate_streams()
    r1 = SerialGetSensorLED(status=0)
    r2 = SensorGetSensorLED(status=1, led_setting=2)
    self.assert_getvalue(s.stream, b'')

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        2  )
    assert s.buffer            == rb1
    assert x is None

    self.write_direct(b, s, rb2)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        2      )
    assert s.buffer            == rb1

    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        3      )
    assert s.buffer            == b''
    assert x == SensorGetSensorLED(status=1, led_setting=2)

  def test_partialReadSerialNonzerostatusAndSensorReply(self):
    b, s = self.generate_streams()
    r1 = SerialGetSensorLED(status=1)
    r2 = SensorGetSensorLED(status=0, led_setting=2)
    self.assert_getvalue(s.stream, b'')

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        2  )
    assert s.buffer            == rb1[1:]
    assert x == SerialGetSensorLED(status=1)

  def test_writeReadReply(self):
    b, s = self.generate_streams()
    w = []
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      r1klass = getSerialReplyByID(cid)
      r1      = r1klass()
      for v in r1:
        r1[v] = 99 # dummy data
      r1.command_id = r1klass.command_id # varibles include this, need to undo it
      if hasattr(r1, "status"):          # the null replies don't have this
        r1.status   = 0                  # set status 0 otherwise we trigger a different check
      print("sending serial %s"%(r1))
      self.sendReply(b, s, r1)
      w.append(r1)
      r2klass = getSensorReplyByID(cid)
      if r2klass:
        r2      = r2klass()
        for v in r2:
          if hasattr(r2, "repeat"):
            if r2.repeat.get(v):
              r2[v] = [99]*99
              r2[r2.repeat[v]] = 99
            else:
              r2[v] = 99 # dummy data
          else:
            r2[v] = 99 # dummy data
        r2.command_id = r2klass.command_id # varibles include this, need to undo it
        if hasattr(r1, "status"):          # the null replies don't have this
          r2.status   = 0                  # set status 0 otherwise we trigger a different check
        print("sending sensor %s"%(r1))
        self.sendReply(b, s, r2)
        w.append(r2)
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      r1 = s.receiveReply(cid)
      print("received %s"%(r1))
      r2 = w.pop(0)
      print("popped %s"%(r2))
      if getSensorReplyByID(cid):
        # If there's a sensor reply, we'll only get that half back with this call,
        #   never the serial reply portion
        r2 = w.pop(0)
        print("popped additional %s"%(r2))
      assert r1 == r2

  # Note: all of these are here so we can override them in the emulator test and change where we're
  # pushing and pulling the data from/to:

  def seek(self, stream, pos):
    return stream.stream.seek(pos)

  def write_underlying(self, b, s, *args, **kwargs):
    return b.write(*args, **kwargs)

  def write_direct(self, b, s, *args, **kwargs):
    return s.write(*args, **kwargs)

  def sendCommand(self, b, s, *args, **kwargs):
    return s.sendCommand(*args, **kwargs)

  def sendReply(self, b, s, *args, **kwargs):
    return s.sendCommand(*args, **kwargs)

  def assert_getvalue(self, stream, value):
    assert stream.getvalue() == value

  def assert_readpos(self, stream, pos):
    assert stream.readpos == pos

















