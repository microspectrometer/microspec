from chromaspeclib.internal.jsonparse import enclassJsonFile
from chromaspeclib.logger             import CHROMASPEC_LOGGER_DATA as log
from chromaspeclib                    import CHROMASPEC_ROOTDIR
import os

CHROMASPEC_SERIAL_ID, CHROMASPEC_SERIAL_NAME = \
  enclassJsonFile(
    os.path.join(
      CHROMASPEC_ROOTDIR,
      "cfg",
      "chromaspec.json"
    ),
    "serial"
  )

globals().update([v.name,v] for k,v in CHROMASPEC_SERIAL_ID.items())

__all__ = list(CHROMASPEC_SERIAL_NAME.keys())+["getSerialReplyByID","getSerialReplyByName"]

def getSerialReplyByID(cid):
  log.info("cid=%d", cid)
  com = CHROMASPEC_SERIAL_ID.get(cid)
  log.info("return %s", com)
  return com

def getSerialReplyByName(name):
  log.info("name=%s", name)
  com = CHROMASPEC_SERIAL_NAME.get(name)
  log.info("return %s", com)
  return com

