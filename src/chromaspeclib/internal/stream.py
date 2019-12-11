from .data   import *
from .logger import CHROMASPEC_LOGGER_STREAM as log
from struct  import pack, unpack
from io      import BytesIO

CHROMASPEC_MAX_READBUFLEN = len(bytes(
  SensorCaptureFrame(pixels=[1]*32765,num_pixels=32765,status=0)
))

class ChromationStream(object):
  def __init__( self, stream ):
    log.info("stream=%s", stream)
    self.stream = stream
    self.buffer = b''

  def read( self, bytelen=0, *args, **kwargs ):
    log.info("bytelen=%d args=%s kwargs=%s", bytelen, args, kwargs)
    if bytelen:
      if bytelen > len(self.buffer):
        self.buffer += self.stream.read( bytelen-len(self.buffer), *args, **kwargs )
      log.info("return buffer[:%d]=%s",bytelen,self.buffer[:bytelen])
      return self.buffer[:bytelen]
    else:
      self.buffer += self.stream.read( *args, **kwargs )
      log.info("return buffer=%s",self.buffer)
      return self.buffer

  def consume( self, bytelen ):
    log.info("bytelen=%d", bytelen)
    self.buffer = self.buffer[bytelen:]

  def pushback( self, buf ):
    log.info("buf=%d", buf)
    self.buffer = buf + self.buffer

  def write( self, buf, *args, **kwargs ):
    log.info("buf=%s args=%s kwargs=%s", buf, args, kwargs)
    self.buffer = b''
    buf = self.stream.write( bytes(buf), *args, **kwargs )
    log.info("return buf=%s", buf)
    return buf

  def receiveCommand( self ):
    log.info("")
    command_id = self.read(1)
    if len(command_id) < 1:
      log.info("Did not read one byte of command_id")
      return None
    klass = getCommandByID( unpack(b'B', command_id)[0] )
    if not klass:
      log.error("Command ID not recognized: %d", command_id)
      return None
    command = klass()
    buf = command_id + self.read( len(command) - 1 )
    if len(buf) < len(command):
      log.info("Read only %d of %d bytes", len(buf), len(command))
      return None
    try:
      command.unpack( buf )
    except Exception as e:
      log.info("Cannot unpack buf=%s exception=%s", buf, str(e))
      return None
    self.consume( len(command) )
    log.info("return %s", command)
    return command

  def sendCommand( self, command ):
    log.info("command=%s", command)
    return self.write( command )

  def sendReply( self, reply ):
    log.info("reply=%s", reply)
    return self.write( reply )

  def receiveReply( self, command_id ):
    log.info("command_id=%d", command_id)
    serial_klass = getSerialReplyByID( command_id )
    sensor_klass = getSensorReplyByID( command_id )
    if not serial_klass:
      log.error("Command ID not recognized: %d", command_id)
      return None
    serialbuf = self.read( CHROMASPEC_MAX_READBUFLEN )
    log.info("serialbuf=%s", serialbuf)
    try:
      serial_reply = serial_klass( serialbuf )
    except Exception as e:
      log.info("serialbuf=%s exception=%s", serialbuf, str(e))
      return None
    self.consume( len(bytes(serial_reply)) )
    if serial_reply.status != 0 or not sensor_klass:
      log.info("return serial_reply=%s", serial_reply)
      return serial_reply
    sensorbuf = self.read( CHROMASPEC_MAX_READBUFLEN )
    log.info("serialbuf=%s", sensorbuf)
    try:
      sensor_reply = sensor_klass( sensorbuf )
    except Exception as e:
      log.info("serialbuf=%s exception=%s pushing back serialbuf=%s", 
        sensorbuf, str(e), serialbuf)
      self.pushback(serialbuf)
      return None
    self.consume( len(bytes(sensor_reply)) )
    log.info("return sensor_reply=%s", sensor_reply)
    return sensor_reply

# Single-threaded test functionality, assumes no partially
# interleaved reading and writing
class ChromationBytesIOStream(ChromationStream):
  def __init__( self, stream=None ):
    log.info("stream=%s", stream)
    if not stream:
      stream = BytesIO()
    self.readpos  = 0
    self.writepos = 0
    super().__init__( stream )

  def read( self, bytelen=0, *args, **kwargs ):
    log.info("args=%s kwargs=%s", args, kwargs)
    log.info("readpos=%d", self.readpos)
    self.stream.seek( self.readpos )
    buf = super().read( bytelen=bytelen, *args, **kwargs )
    self.readpos += len(buf)
    log.info("return buf=%s", buf)
    return buf

  def write( self, buf, *args, **kwargs ):
    log.info("buf=%s args=%s kwargs=%s", buf, args, kwargs)
    log.info("writepos=%d", self.writepos)
    self.stream.seek( self.writepos )
    result = super().write( bytes(buf), *args, **kwargs )
    self.writepos += result
    log.info("return result=%d", result)
    return result

  def sendReply( self, reply ):
    log.info("reply=%s", reply)
    result = self.write( reply )
    log.info("return result=%d", result)
    return result

# TODO: ChromationSerialIOStream

