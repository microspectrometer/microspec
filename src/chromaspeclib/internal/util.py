from .logger import CHROMASPEC_LOGGER_UTIL as log
from struct  import unpack, pack

class ChromationInteger(int):
  def __new__( self, value, size=1, byteorder="big", signed=False ):
    log.info("value=%d size=%d byteorder=%s signed=%s", value, size, byteorder, signed)
    self = int.__new__( ChromationInteger, value )
    self.size      = size
    self.byteorder = byteorder
    self.signed    = signed
    log.info("return %s", self)
    return self

  def __bytes__( self ):
    log.info("")
    b = self.to_bytes( self.size, self.byteorder, self.signed )
    log.info("return %s", b)

def isInt( i ):
  log.info("int=%s", i)
  try:
    if int(i) == i:
      log.info("return True")
      return True
  except:
    log.info("return False")
    return False

