
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from chromaspeclib.logger import CHROMASPEC_LOGGER_JSON as log
from .payload import ChromaSpecPayloadClassFactory as cfactory
from .util    import dehex
import json

def globalizeJsonFile(filename):
  log.info("filename=%s", filename)
  with open(filename) as f:
    j = json.load(f)["globals"]
    log.debug("raw json=%s", j)
    jobjects = dict([k,dehex(v)] for k,v in j.items())
    log.info("return %s", jobjects)
    return jobjects
  
def enclassJsonFile(filename, protocol="command"):
  log.info("filename=%s protocol=%s", filename, protocol)
  with open(filename) as f:
    j      = json.load(f)
    p      = j["protocol"][protocol]
    byID   = {}
    byName = {}
    log.debug("raw json=%s", j)
    log.debug("raw json protocol section=%s", p)
    for k, v in p.items():
      log.debug("k=%s v=%s", k, v)
      c = cfactory(protocol, int(k), protocol.capitalize()+p[k]["name"], 
                   p[k]["variables"], p[k]["sizes"], p[k].get("repeat",None))
      byID[c.command_id] = c
      byName[c.name] = c
  log.info("return %s, %s", byID, byName)
  return byID, byName
