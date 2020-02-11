from chromaspeclib.datatypes  import *
from chromaspeclib.logger     import CHROMASPEC_LOGGER_STREAM as log
from chromaspeclib.exceptions import ChromaSpecConnectionException, ChromaSpecEmulationException
from struct       import pack, unpack
from io           import BytesIO
from serial       import Serial
from serial.tools import list_ports

import subprocess
import tempfile
import atexit
import select
import sys 
import os

class ChromaSpecStream(object):
  def __init__(self, stream):
    log.info("stream=%s", stream)
    self.stream = stream
    self.buffer = b''
    log.info("return")

  def read(self, bytelen=0, *args, **kwargs):
    log.info("bytelen=%s args=%s kwargs=%s", bytelen, args, kwargs)
    if bytelen:
      if bytelen > len(self.buffer):
        self.buffer += self.stream.read(bytelen-len(self.buffer), *args, **kwargs)
      log.info("return buffer[:%s]=%s",bytelen,self.buffer[:bytelen])
      return self.buffer[:bytelen]
    else:
      self.buffer += self.stream.read(*args, **kwargs)
      log.info("return buffer=%s",self.buffer)
      return self.buffer

  def consume(self, bytelen):
    log.info("bytelen=%s", bytelen)
    self.buffer = self.buffer[bytelen:]
    log.info("return")

  def pushback(self, buf):
    log.info("buf=%s", buf)
    self.buffer = buf + self.buffer
    log.info("return")

  def write(self, buf, *args, **kwargs):
    log.info("buf=%s args=%s kwargs=%s", buf, args, kwargs)
    buf = self.stream.write(bytes(buf), *args, **kwargs)
    log.info("return buf=%s", buf)
    return buf

  def receiveCommand(self):
    log.info("read 1")
    command_id = self.read(1)
    if len(command_id) < 1:
      log.info("Did not read one byte of command_id")
      return None
    klass = getCommandByID(unpack(b'B', command_id)[0])
    if not klass:
      log.error("Command ID not recognized: %s", command_id)
      return None
    command = klass()
    self.consume(1)
    if len(command) > 1:
      buf = command_id + self.read(len(command) - 1)
    else:
      buf = command_id
    if len(buf) < len(command):
      log.info("Read only %s of %s bytes", len(buf), len(command))
      self.pushback(command_id)
      return None
    try:
      log.info("unpack %s", buf)
      command.unpack(buf)
    except Exception as e:
      log.info("Cannot unpack buf=%s exception=%s", buf, str(e))
      return None
    self.consume(len(command) - 1)
    log.info("return %s", command)
    return command

  def sendCommand(self, command):
    log.info("command=%s", command)
    return self.write(command)

  def sendReply(self, reply):
    log.info("reply=%s", reply)
    result = self.write(reply)
    log.info("return result=%s", result)
    return result

  def receiveReply(self, command_id):
    log.info("command_id=%s", command_id)
    serial_klass = getSerialReplyByID(command_id)
    sensor_klass = getSensorReplyByID(command_id)
    if not serial_klass:
      log.error("Command ID not recognized: %s", command_id)
      return None
    if serial_klass is SerialNull:
      log.info("serial reply is SerialNull")
      return serial_klass()
    serialbuf = self.read(0)
    log.info("serialbuf=%s", serialbuf)
    try:
      serial_reply = serial_klass(serialbuf)
    except Exception as e:
      log.info("serialbuf=%s exception=%s", serialbuf, str(e))
      return None
    if not hasattr(serial_reply, "status") or serial_reply.status is None:
      log.info("serial reply is empty")
      return None
    seriallen = len(bytes(serial_reply))
    self.consume(seriallen)
    serialbuf = serialbuf[0:seriallen]
    if serial_reply.status != 0 or not sensor_klass:
      log.info("return serial_reply=%s", serial_reply)
      return serial_reply
    sensorbuf = self.read(0)
    log.info("serialbuf=%s", sensorbuf)
    try:
      sensor_reply = sensor_klass(sensorbuf)
    except Exception as e:
      log.info("sensorbuf=%s exception=%s pushing back serialbuf=%s", 
        sensorbuf, str(e), serialbuf)
      self.pushback(serialbuf)
      return None
    if sensor_reply.status is None:
      log.info("sensor reply is empty")
      self.pushback(serialbuf)
      return None
    self.consume(len(bytes(sensor_reply)))
    log.info("return sensor_reply=%s", sensor_reply)
    return sensor_reply

# Single-threaded test functionality, assumes no partially
# interleaved reading and writing by multiple threads
class ChromaSpecBytesIOStream(ChromaSpecStream):
  def __init__(self, stream=None):
    log.info("stream=%s", stream)
    if not stream:
      stream = BytesIO()
    self.readpos  = 0
    self.writepos = 0
    super().__init__(stream)

  def read(self, bytelen=0, *args, **kwargs):
    log.info("bytelen=%s args=%s kwargs=%s", bytelen, args, kwargs)
    log.info("readpos=%s", self.readpos)
    self.stream.seek(self.readpos)
    pre  = self.stream.tell()
    buf  = super().read(bytelen=bytelen, *args, **kwargs)
    post = self.stream.tell()
    self.readpos += post - pre
    log.info("return buf=%s", buf)
    return buf

  def write(self, buf, *args, **kwargs):
    log.info("buf=%s args=%s kwargs=%s", buf, args, kwargs)
    log.info("writepos=%s", self.writepos)
    self.stream.seek(self.writepos)
    result = super().write(bytes(buf), *args, **kwargs)
    self.writepos += result
    log.info("return result=%s", result)
    return result

class ChromaSpecSerialIOStream(ChromaSpecStream):
  def __init__(self, serial_number=None, device=None, timeout=0, *args, **kwargs):
    log.info("serial_number=%s device=%s timeout=%s args=%s kwargs=%s", serial_number, device, timeout, args, kwargs)
    self.serial          = Serial(*args, **kwargs)
    self.serial.baudrate = 115200
    self.serial.timeout  = timeout
    self.serial.port     = None
    if serial_number:
      self.serial.port = list_ports.grep(serial_number).device
      log.info("search for serial_number=%s found port=%s", serial_number, port)
    elif device:
      self.serial.port = device
      log.info("using device=%s", device)
    else:
      ports = list(list_ports.grep("CHROMATION"))
      if ports:
        self.serial.port = ports[0].device
        log.info("defaulting to searching for CHROMATION hardware, found port=%s", self.serial.port)
      if not self.serial.port:
        for port in list_ports.comports(True):
          if port.vid == 1027 and port.pid == 24597:
            self.serial.port = port.device
            break
      if not self.serial.port:
        log.error("Cannot find CHROMATION device")
        raise ChromaSpecConnectionException("Cannot find CHROMATION device")
    try:
      self.serial.open()
    except Exception as e:
      log.error("Cannot open device: check if port is already in use, such as another ChromaSpec interface is using it: %s"%(e))
      raise ChromaSpecConnectionException(str(e))
    super().__init__(self.serial)
    log.info("return")

  def read(self, bytelen=0, *args, **kwargs):
    log.info("bytelen=%s args=%s kwargs=%s", bytelen, args, kwargs)
    if not bytelen:
      waiting  = self.stream.inWaiting()
      inbuffer = len(self.buffer)
      waitfor  = waiting+inbuffer
      log.info("serial stream bytelen=%s waiting=%s inbuffer=%d setting to %s", bytelen, waiting, inbuffer, waitfor)
      bytelen = waitfor
    return super().read(bytelen, *args, **kwargs)

class ChromaSpecEmulatedStream(ChromaSpecSerialIOStream):
  def __init__(self, hardware=None, software=None, timeout=None, socat=False, fork=False, *args, **kwargs):
    log.info("hardware=%s software=%s timeout=%s args=%s kwargs=%s", hardware, software, timeout, args, kwargs)
    cleanup_hardware = False
    cleanup_software = False
    cleanup_tempdir  = False

    if not hardware or not software:
      tempdir = tempfile.mkdtemp()
      cleanup_tempdir = True

    if not hardware:
      hardware = os.path.join(tempdir, "chromation.hardware")
      cleanup_hardware = True

    if not software:
      software = os.path.join(tempdir, "chromation.software")
      cleanup_software = True

    if socat:
      log.info("forking socat process")
      #TODO: make this work for PC as well as MAC
      # Note: the -D is there to print something, anything, to stderr, so we can wait for it
      socat = subprocess.Popen(["socat", "-D", "PTY,raw,echo=0,link=%s"%(hardware),
                                               "PTY,raw,echo=0,link=%s"%(software)],
                               stderr=subprocess.PIPE)
  
      # Wait at most a second for socat to come up and announce itself, by which time the
      # files it needs to create should be there:
      r, w, x = select.select([socat.stderr],[],[],1)
      #import pdb; pdb.set_trace();
      if not r:
        raise ChromaSpecEmulationException("Cannot create socat process to mediate USB emulation!")
  
      def cleanup():
        log.warning("Cleanup: killing socat process")
        socat.kill()
        if cleanup_hardware:
          try:
            log.warning("Cleanup: removing hardware file %s"%(hardware))
            os.remove(hardware)
          except:
            pass # possibly a race condition with socat dying and not removing this quickly enough
        if cleanup_software:
          try:
            log.warning("Cleanup: removing software file %s"%(software))
            os.remove(software)
          except:
            pass # possibly a race condition with socat dying and not removing this quickly enough
        if cleanup_tempdir:
          if os.path.isdir(tempdir):
            log.warning("Cleanup: removing temp directory %s"%(tempdir))
            os.rmdir(tempdir)
        log.warning("Cleanup: done")
      atexit.register(cleanup)
      self.socat = socat

    if fork:
      log.info("forking emulator process")
      # -p so that we can capture the stdout to make sure it's up and running
      fork = subprocess.Popen(["chromaspec_emulator.py", "-t", "10", "-p", "-f", hardware],
                              stdout=subprocess.PIPE)

      # Wait at most a second for emulator to come up and announce itself, by which time it
      # should have it's socket open and waiting
      r, w, x = select.select([fork.stdout],[],[],1)
      #import pdb; pdb.set_trace();
      if not r:
        raise ChromaSpecEmulationException("Cannot create emulator process for USB emulation!")
  
      def cleanup():
        log.warning("Cleanup: killing emulator process")
        fork.kill()
        log.warning("Cleanup: done")
      atexit.register(cleanup)
      self.fork = fork

    self.hardware = hardware
    self.software = software

    super().__init__(device=hardware, timeout=timeout)
