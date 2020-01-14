import unittest, os
from chromaspeclib.internal.jsonparse import globalizeJsonFile, enclassJsonFile

jsontest = os.path.realpath( os.path.join( os.path.dirname( __file__ ), "test.json" ) )

class ChromaSpecTestJson(unittest.TestCase):

  def test_globals(self):
    g = globalizeJsonFile( jsontest )
    assert g["hex"]    == 255
    assert g["int"]    == 256
    assert g["string"] == "foo"
    assert g["bool"]   == False

  def test_command(self):
    cid, cname = enclassJsonFile( jsontest, protocol="command" )
    assert cid  [0         ]().name         == "Commanda"
    assert cid  [1         ]().variables[0] == "command_id"
    assert cid  [2         ]().sizes[2]     == 4
    assert cid  [2         ]().repeat["b"]  == "a"
    assert cname["Commanda"]().name         == "Commanda"
    assert cname["Commandb"]().variables[0] == "command_id"
    assert cname["Commandc"]().sizes[2]     == 4
    assert cname["Commandc"]().repeat["b"]  == "a"

  def test_serial(self):
    cid, cname = enclassJsonFile( jsontest, protocol="serial" )
    assert cid  [0        ]().name         == "Seriala"
    assert cid  [1        ]().variables[0] == "command_id"
    assert cid  [2        ]().sizes[2]     == 4
    assert cid  [2        ]().repeat["b"]  == "a"
    assert cname["Seriala"]().name         == "Seriala"
    assert cname["Serialb"]().variables[0] == "command_id"
    assert cname["Serialc"]().sizes[2]     == 4
    assert cname["Serialc"]().repeat["b"]  == "a"

  def test_sensor(self):
    cid, cname = enclassJsonFile( jsontest, protocol="sensor" )
    assert cid  [0         ]().name         == "Sensora"
    assert cid  [1         ]().variables[0] == "command_id"
    assert cid  [2         ]().sizes[2]     == 4
    assert cid  [2         ]().repeat["b"]  == "a"
    assert cname["Sensora"]().name         == "Sensora"
    assert cname["Sensorb"]().variables[0] == "command_id"
    assert cname["Sensorc"]().sizes[2]     == 4
    assert cname["Sensorc"]().repeat["b"]  == "a"

