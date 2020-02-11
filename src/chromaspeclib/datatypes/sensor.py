from chromaspeclib.internal.jsonparse import enclassJsonFile
from chromaspeclib.logger             import CHROMASPEC_LOGGER_DATA as log
from chromaspeclib                    import CHROMASPEC_ROOTDIR
import os

CHROMASPEC_SENSOR_ID, CHROMASPEC_SENSOR_NAME = \
  enclassJsonFile(
    os.path.join(
      CHROMASPEC_ROOTDIR,
      "cfg",
      "chromaspec.json"
    ),
    "sensor"
  )

globals().update([v.name,v] for k,v in CHROMASPEC_SENSOR_ID.items())

__all__ = list(CHROMASPEC_SENSOR_NAME.keys())+["getSensorReplyByID","getSensorReplyByName"]

def getSensorReplyByID(cid):
  log.info("cid=%d", cid)
  com = CHROMASPEC_SENSOR_ID.get(cid)
  log.info("return %s", com)
  return com

def getSensorReplyByName(name):
  log.info("name=%s", name)
  com = CHROMASPEC_SENSOR_NAME.get(name)
  log.info("return %s", com)
  return com

