import unittest, os
from chromaspeclib.internal.payload import ChromationPayloadClassFactory, ChromationPayload, ChromationRepeatPayload

class ChromaspecTestPayloadFactory(unittest.TestCase):

  def test_payloadFactoryNormal(self):
    klass = ChromationPayloadClassFactory( 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4] )
    assert klass.command_id == 99
    assert klass.__name__   == "grok"
    assert klass.variables  == ["command_id","foo","bar","baz"]
    assert klass.sizes      == [1,1,2,4]

  def test_payloadFactoryRepeat(self):
    klass = ChromationPayloadClassFactory( 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4], repeat={"foo":"bar"} )
    assert klass.command_id == 99
    assert klass.__name__   == "grok"
    assert klass.variables  == ["command_id","foo","bar","baz"]
    assert klass.sizes      == [1,1,2,4]
    assert klass.repeat     == {"foo":"bar"}

class ChromaspecTestPayload(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(ChromaspecTestPayload, self).__init__(*args, **kwargs)
    self.klass = ChromationPayloadClassFactory( 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4] )

  def test_initEmpty(self):
    obj = self.klass()
    assert obj.foo        == None
    assert obj.bar        == None
    assert obj.baz        == None
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_initKwargs(self):
    obj = self.klass(foo=1,bar=2,baz="0xFF")
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_initPayload(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_unpack(self):
    obj = self.klass()
    obj.unpack(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_iter(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    var = []
    for v in obj:
      var.append(v)
    assert var == ["command_id","foo","bar","baz"]

  def test_str(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    s   = """<grok name=grok command_id=99 variables=['command_id', 'foo', 'bar', 'baz'] values={'command_id': 99, 'foo': 1, 'bar': 2, 'baz': 255} sizes=[1, 1, 2, 4] packformat=>BBHL length=8 packed=b'c\\x01\\x00\\x02\\x00\\x00\\x00\\xff'>"""
    assert str(obj) == s

  def test_bytes(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert bytes(obj) == b

  def test_len(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert len(bytes(obj)) == len(b)

  def test_packformat(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.packformat() == ">BBHL"

  def test_packvalues(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.packvalues() == [ 99, 1, 2, 255 ]

  def test_pack(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert obj.pack() == b

class ChromaspecTestRepeatPayload(ChromaspecTestPayload):

  def __init__(self, *args, **kwargs):
    super(ChromaspecTestRepeatPayload, self).__init__(*args, **kwargs)
    self.klass = ChromationPayloadClassFactory( 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4], repeat={"baz": "foo"} )

  def test_initEmpty(self):
    obj = self.klass()
    assert obj.foo        == None
    assert obj.bar        == None
    assert obj.baz        == []
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == { "baz": "foo" }

  def test_initKwargs(self):
    obj = self.klass(foo=1,bar=2,baz=["0xFF"])
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == [255]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == { "baz": "foo" }

  def test_initPayload(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == [255]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == { "baz": "foo" }

  def test_unpack(self):
    obj = self.klass()
    obj.unpack(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == [255]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_str(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    s   = """<grok name=grok command_id=99 variables=['command_id', 'foo', 'bar', 'baz'] values={'command_id': 99, 'foo': 1, 'bar': 2, 'baz': [255]} sizes=[1, 1, 2, 4] packformat=>BBHL length=8 packed=b'c\\x01\\x00\\x02\\x00\\x00\\x00\\xff'>"""
    assert str(obj) == s












