from chromaspeclib.internal.stream import *
from chromaspeclib.internal.logger import CHROMASPEC_LOGGER as log
from chromaspeclib.internal.data   import CommandNull
import time

# The intended difference between this and the Simple interface is to provide more
# fine control, such as breaking up sending commands and then looping to wait for
# replies. It requires creating Command objects and then passing them along, in 
# contrast to the one routine per command structure of the Simple interface.

class ChromaSpecExpertInterface(ChromaSpecSerialIOStream):
  def __init__(self, serial_number=None, device=None, timeout=0.01, retry_timeout=0.001, *args, **kwargs):
    log.info("serial_number=%s, device=%s, timeout=%s, retry_timeout=%s, args=%s, kwargs=%s",
             serial_number, device, timeout, retry_timeout, args, kwargs)
    super().__init__(serial_number=serial_number, 
                     device=device, timeout=timeout, 
                     *args, **kwargs)
    self.retry_timeout = retry_timeout
    self.current_command = []
    log.info("return")

  def __setattr__(self, attr, value):
    if attr == "timeout":
      log.info("set timeout to %s", value)
      self.stream.timeout = value
    else:
      self.__dict__[attr] = value
      
  def __getattribute__(self, attr):
    if attr == "timeout":
      log.info("return timeout=%s", self.stream.timeout)
      return self.stream.timeout
    else:
      return super().__getattribute__(attr)
      
  def sendCommand(self, command):
    log.info("command=%s", command)
    self.current_command.append(command)
    super().sendCommand(command)
    log.info("return")

  def receiveReply(self):
    log.info("waiting for reply")
    if not self.current_command:
      log.error("No command to wait for")
    start = time.time()
    reply = super().receiveReply(self.current_command[0].command_id)
    since = time.time() - start
    timeout = self.timeout if self.timeout else 0
    remain = timeout - since
    while not reply and remain > 0:
      log.info("no reply yet, timeout remaining=%s", remain)
      time.sleep( self.retry_timeout if remain > self.retry_timeout else remain )
      reply = super().receiveReply(self.current_command[0].command_id)
      since = time.time() - start
      remain = timeout - since
    if reply:
      log.info("popping command since reply was found")
      self.current_command.pop(0)
    log.info("return %s", reply)
    return reply

  def sendAndReceive(self, command):
    self.sendCommand(command)
    reply = self.receiveReply()
    if not reply:
      log.info("popping command anyways since reply was not found")
      self.current_command.pop(0)
    log.info("return %s", reply)
    return reply

  def flush(self, timeout=0.1):
    log.info("flushing stream by sending a null and clearing all data from the line")
    self.sendCommand(CommandNull())
    old_timeout = self.timeout
    self.timeout = timeout
    self.read(None)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.timeout = old_timeout
    self.current_command = []
