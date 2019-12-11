import serial
import serial.tools.list_ports as list_ports

class ChromationConnection( serial.Serial ):
  def __init__( self, serial_number=None, device=None, file=None, emulation=False, timeout=0, *args, **kwargs ):
    serial.Serial.__init__( self, *args, **kwargs )
    self.baudrate = 115200
    self.timeout  = timeout
    if serial_number:
      self.port = list_ports.grep(serial_number).device
    elif device:
      self.port = device
    elif file:
      self.port = file
    elif emulation:
      raise Exception("Not supported yet")

