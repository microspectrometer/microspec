import unittest, os, pytest
from io import BytesIO
from chromaspeclib.internal.stream       import ChromaSpecBytesIOStream
from chromaspeclib.internal.data         import *
from chromaspeclib.internal.data.command import CHROMASPEC_COMMAND_ID

#from chromaspeclib.internal.logger import CHROMASPEC_LOGGER_STREAM
#import logging
#CHROMASPEC_LOGGER_STREAM.setLevel(logging.DEBUG)

class ChromaSpecTestBytesIOStream(unittest.TestCase):

  def test_defaultStream(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream()
    assert b is not s.stream

  def test_parameterStream(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    assert b is s.stream

  def test_underlyingStreamRead1(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read(1)
    assert d[0] == r[0]
    assert len(r) == 1

  def test_underlyingStreamRead1Fail(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b''
    b.write(d)
    r = s.read(1)
    assert len(r) == 0

  def test_underlyingStreamReadAll(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read()
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamReadManyFail(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    b.write(d)
    r = s.read(10)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamWrite(self):
    b = BytesIO()
    s = ChromaSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    s.write(d)
    b.seek(0)
    w = b.read()
    assert     w  ==     d
    assert len(w) == len(d)

  def test_write1Read1(self):
    s = ChromaSpecBytesIOStream()
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
    s = ChromaSpecBytesIOStream()
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
    s = ChromaSpecBytesIOStream()
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

  def test_writeManyReadInterleaved(self):
    s = ChromaSpecBytesIOStream()
    d = b'\x00\x01\x02\x03\x04\x05'
    s.write(d[0:3])
    r = s.read(1)
    assert     r  ==     d[0:1]
    assert len(r) == len(d[0:1])
    s.write(d[3:4])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[1:2]
    assert len(r) == len(d[1:2])
    s.consume(1)
    s.write(d[4:5])
    r = s.read(1)
    assert     r  ==     d[2:3]
    assert len(r) == len(d[2:3])
    s.consume(1)
    r = s.read(1)
    s.write(d[5:6])
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
    s = ChromaSpecBytesIOStream()
    d = b'\x00\x01\x02\x03\x04\x05'
    s.write(d)
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
    s = ChromaSpecBytesIOStream()
    w = []
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      cklass = getCommandByID(cid)
      c      = cklass()
      for v in c:
        c[v] = 99 # dummy data
      c.command_id = cklass.command_id # varibles include this, need to undo it
      s.sendCommand(c)
      w.append(c)
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      c1 = s.receiveCommand()
      c2 = w.pop(0)
      assert c1 == c2

  def test_partialReadCommand(self):
    s = ChromaSpecBytesIOStream()
    c = CommandGetBridgeLED(led_num=0)
    assert s.stream.getvalue() == b''

    cb = bytes(c)
    cb1 = cb[0:len(cb)-1]
    cb2 = cb[len(cb)-1:]
    s.write(cb1)
    assert s.buffer            == b''
    assert s.stream.getvalue() == cb1
    assert s.readpos           == 0

    r = s.receiveCommand()
    assert s.buffer            == cb1
    assert s.stream.getvalue() == cb1
    assert s.readpos           == 1
    assert r is None

    s.write(cb2)
    assert s.buffer            == cb1
    assert s.stream.getvalue() == cb1+cb2
    assert s.readpos           == 1

    r = s.receiveCommand()
    assert s.buffer            == b''
    assert s.stream.getvalue() == cb1+cb2
    assert s.readpos           == 2
    assert r == CommandGetBridgeLED(led_num=0)

  def test_partialReadSerialReply(self):
    s = ChromaSpecBytesIOStream()
    r = SerialGetBridgeLED(status=0, led_num=0, led_setting=1)
    assert s.stream.getvalue() == b''

    rb = bytes(r)
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    s.write(rb1)
    assert s.buffer            == b''
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 0

    x = s.receiveReply(r.command_id)
    assert s.buffer            == rb1
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 1
    assert x is None

    s.write(rb2)
    assert s.buffer            == rb1
    assert s.stream.getvalue() == rb1+rb2
    assert s.readpos           == 1

    x = s.receiveReply(r.command_id)
    assert s.buffer            == b''
    assert s.stream.getvalue() == rb1+rb2
    assert s.readpos           == 2
    assert x == SerialGetBridgeLED(status=0, led_num=0, led_setting=1)

  def test_partialReadSerialAndSensorReply(self):
    s = ChromaSpecBytesIOStream()
    r1 = SerialGetSensorLED(status=0)
    r2 = SensorGetSensorLED(status=1, led_setting=2)
    assert s.stream.getvalue() == b''

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    s.write(rb1)
    assert s.buffer            == b''
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 0

    x = s.receiveReply(r1.command_id)
    assert s.buffer            == rb1
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 2
    assert x is None

    s.write(rb2)
    assert s.buffer            == rb1
    assert s.stream.getvalue() == rb1+rb2
    assert s.readpos           == 2

    x = s.receiveReply(r1.command_id)
    assert s.buffer            == b''
    assert s.stream.getvalue() == rb1+rb2
    assert s.readpos           == 3
    assert x == SensorGetSensorLED(status=1, led_setting=2)

  def test_partialReadSerialNonzerostatusAndSensorReply(self):
    s = ChromaSpecBytesIOStream()
    r1 = SerialGetSensorLED(status=1)
    r2 = SensorGetSensorLED(status=0, led_setting=2)
    assert s.stream.getvalue() == b''

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    s.write(rb1)
    assert s.buffer            == b''
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 0

    x = s.receiveReply(r1.command_id)
    assert s.buffer            == rb1[1:]
    assert s.stream.getvalue() == rb1
    assert s.readpos           == 2
    assert x == SerialGetSensorLED(status=1)

  def test_writeReadReply(self):
    s = ChromaSpecBytesIOStream()
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
      s.sendReply(r1)
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
        s.sendReply(r2)
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

















