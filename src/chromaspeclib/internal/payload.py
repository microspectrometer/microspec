from .util   import *
from .logger import CHROMASPEC_LOGGER_PAYLOAD as log
from struct  import unpack, pack

class ChromaSpecPayload(object):
  def __init__( self, payload=None, **kwargs ):
    log.info("payload=%s kwargs=%s", payload, kwargs)
    # If we don't make a copy of these, editing them edits the class copy.
    # One should not be changing them, but if one does, one shouldn't break everything,
    #   and merely making them read-only doesn't fix the issue of mutable sub-objects.
    self.__dict__["command_id"] = self.__class__.command_id
    self.__dict__["variables"]  = self.__class__.variables.copy()
    self.__dict__["sizes"]      = self.__class__.sizes.copy()
    self.value   = {}
    self.varsize = {}
    for n in range( 0, len(self.variables) ):
      log.debug("n=%d", n)
      var   = self.variables[n]
      value = kwargs.get( var, None )
      # Use __setitem__ rather than .value[var] to utilize casting functionality
      #   and set size first because it's part of the ChromaSpecInteger casting
      self.varsize[var] = self.sizes[n]
      self[        var] = value 
      log.debug("value[%s]=%s size[%s]=%d", var, value, var, self.sizes[n])
    if "command_id" in self.value:
      self["command_id"] = self.command_id
    if payload:
      self.unpack(payload)
    log.info("return")

  def __getitem__( self, attr ):
    log.info("attr=%s", attr)
    if attr != "variables" and attr in self.variables:
      log.info("return %s", self.__dict__["value"][attr])
      return self.__dict__["value"][attr]
    elif attr not in self.__dict__:
      log.error("Attribute %s not found in payload object", attr)
      raise AttributeError
    else:
      log.info("return %s", self.__dict__[attr])
      return self.__dict__[attr]

  def __setitem__( self, attr, value ):
    log.info("attr=%s value=%s", attr, value)
    if attr != "variables" and attr in self.variables:
      self.__dict__["value"].update({attr:
        value if value is None else 
        ChromaSpecInteger( dehex(value), self.varsize[attr] ) 
      })
    else:
      self.__dict__.update({attr: value})
    log.info("return")

  def __iter__( self ):
    log.info("return")
    return iter(self.variables)

  def __setattr__( self, attr, value ):
    log.info("attr=%s value=%s", attr, value)
    if attr != "variables" and attr in self.variables:
      self.__dict__["value"].update({attr:
        value if value is None else 
        ChromaSpecInteger( dehex(value), self.varsize[attr] )
      })
    else:
      self.__dict__.update({attr: value})
    log.info("return")

  def __getattr__( self, attr ):
    log.info("attr=%s", attr)
    if attr != "variables" and attr in self.variables:
      return self.__dict__["value"][attr]
    elif attr not in self.__dict__:
      log.error("Attribute %s not found in payload object", attr)
      raise AttributeError
    else:
      return self.__dict__[attr]
    log.info("return")

  def __str__( self ):
    log.info("")
    s = "<%s name=%s command_id=%s variables=%s values=%s sizes=%s packformat=%s length=%d packed=%s>" % \
      ( self.__class__.__name__, self.name, self.command_id, self.variables, \
        self.value, self.sizes, self.packformat(), \
        len(self), self.pack() )
    log.info("return %s", s)
    return s

  def __bytes__( self ):
    log.info("")
    b = self.pack()
    log.info("return %s", b)
    return b

  def __len__( self ):
    log.info("")
    l = sum( self.sizes )
    log.info("return %s", l)
    return l

  def packformat( self ):
    log.info("")
    packformat = ">"
    for v in self.variables:
      log.debug("packformat=%s varsize[%s]=%d", packformat, v, self.varsize[v])
      packformat += "B" if self.varsize[v] == 1 else \
                    "H" if self.varsize[v] == 2 else \
                    "L" if self.varsize[v] == 4 else \
                    str(   self.varsize[v]) + "s"
    log.info("return %s", packformat)
    return packformat

  def packvalues( self ):
    log.info("")
    pv = [ getattr( self, v ) for v in self.variables ]
    log.info("return %s", pv)
    return pv

  def pack( self ):
    log.info("")
    if None in self.value.values():
      log.warning("Marshalling a payload that is missing values, returning ''");
      return b''
    p = pack( self.packformat(), *self.packvalues() )
    log.info("return %s", p)
    return p

  def unpack( self, payload ):
    log.info("payload=%s", payload)
    # The payload may be bigger than needed, to accommodate
    #   chopping data down packet by packet
    length = len(self)
    values = unpack( self.packformat(), payload[0:length] )
    log.debug( "unpacked values=%s", values )
    for n in range( 0, len(values) ):
      log.debug( "variables[%d]=%s <- values[%d]=%s", n, self.variables[n], n, values[n] )
      setattr( self, self.variables[n], values[n] )
    p = payload[length:]
    log.info("return %s", p)
    return p

  def __eq__(self, other):
    if not isinstance(other, ChromaSpecPayload):
      return NotImplemented
    if self.name       != other.name:       return False
    if self.command_id != other.command_id: return False
    if self.variables  != other.variables:  return False
    if self.value      != other.value:      return False
    if self.sizes      != other.sizes:      return False
    if self.varsize    != other.varsize:    return False
    return True

class ChromaSpecRepeatPayload( ChromaSpecPayload ):
  """The difference from the parent class is that the repeat process
  requires packing arrays, and requires partially-gradually unpacking
  the payload, since part of the payload defines how much to continue
  to pack and unpack."""

  def __init__( self, *args, **kwargs ):
    self.__dict__["repeat"] = self.__class__.repeat.copy()
    super().__init__(*args,**kwargs)

  def __setattr__( self, attr, value ):
    log.info("attr=%s value=%s", attr, value)
    if attr != "variables" and attr in self.variables:
      repeat = self.repeat.get( attr, None )
      if repeat:
        self.__dict__["value"].update({attr:
          [] if value is None else
          [ ChromaSpecInteger( dehex(v), self.varsize[attr] ) for v in value ]
        })
      else:
        self.__dict__["value"].update({attr:
          value if value is None else
          ChromaSpecInteger( dehex(value), self.varsize[attr] )
        })
    else:
      self.__dict__.update({attr: value})
    log.info("return")

  def __setitem__( self, attr, value ):
    log.info("attr=%s value=%s", attr, value)
    if attr != "variables" and attr in self.variables:
      repeat = self.repeat.get( attr, None )
      if repeat:
        self.__dict__["value"][attr] = \
          [] if value is None else \
          [ v if v is None else ChromaSpecInteger( dehex(v), self.varsize[attr] ) for v in value ]
      else:
        self.__dict__["value"][attr] = \
          value if value is None else \
          ChromaSpecInteger( dehex(value), self.varsize[attr] )
    else:
      self.__dict__[attr] = value
    log.info("return")

  def packformat( self ):
    log.info("")
    packformat = ">"
    for v in self.variables:
      log.debug("packformat=%s v=%s", packformat, v)
      pf = "B" if self.varsize[v] == 1 else \
           "H" if self.varsize[v] == 2 else \
           "L" if self.varsize[v] == 4 else \
           str(   self.varsize[v]) + "s"
      repeat = self.repeat.get( v, None )
      log.debug("repeat=%s", repeat)
      if repeat:
        repeat_num = self[repeat]
        log.debug("repeat_num=%s", repeat_num)
        pf = pf * int(repeat_num if repeat_num is not None else 1)
      packformat += pf
    log.info("return %s", packformat)
    return packformat

  def packvalues( self ):
    log.info("")
    import itertools
    pv = list( itertools.chain.from_iterable( # flatten repeat items #
             [   getattr( self, v )[0:int(self[self.repeat.get(v)])] 
               if self.repeat.get(v,None) else
                 [ getattr( self, v ) ]
               for v in self.variables ]
           ) )
    log.info("return %s", pv)
    return pv

  def unpack( self, payload ): 
    log.info("payload=%s",payload)
    # The payload may be bigger than needed, to accommodate
    # chopping data down packet by packet
    packformat = super().packformat()
    # The superclass packformat doesn't repeat, so it's used to iterate through
    # the elements one at a time, whereas the pack function can pack everything
    # at once
    endian     = packformat[0]
    packrest   = packformat[1:]
    payrest    = payload[:]
    log.debug("packformat=%s payrest=%s",packformat,payrest)
    used   = 0
    for n in range( 0, len(self.variables) ):
      repeat = self.repeat.get( self.variables[n], None )
      log.debug("packformat=%s payrest=%s n=%d repeat=%s variables[%d]=%s", 
                packformat, payrest, n, repeat, n, self.variables[n])
      if repeat:
        size     = self.sizes[n]
        number   = int(self[repeat])
        packmany = packrest[0] * number
        log.debug("if-repeat size=%d number=%d packmany=%s", size, number, packmany)
        value    = unpack( endian+packmany, payrest[0:size*number] )
        log.debug("value=%s", value)
        used    += size*number
        packrest = packrest[1:]
        payrest  = payrest[size*number:]
        log.debug("used=%d packrest=%s payrest=%s", used, packrest, payrest)
        setattr( self, self.variables[n], value )
      else:
        size     = self.sizes[n]
        log.debug("if-no-repeat size=%d", size)
        value    = unpack( endian+packrest[0], payrest[0:size] )
        log.debug("value=%s", value)
        used    += size
        packrest = packrest[1:]
        payrest  = payrest[size:]
        log.debug("used=%d packrest=%s payrest=%s", used, packrest, payrest)
        setattr( self, self.variables[n], value[0] )
    p = payload[used:]
    log.info("return %s", p)
    return p

  def __eq__(self, other):
    if not isinstance(other, ChromaSpecRepeatPayload):
      log.info("return NotImplemented")
      return NotImplemented
    if not super().__eq__(other):   
      log.info("return False")
      return False
    if self.repeat != other.repeat: 
      log.info("return False")
      return False
    log.info("return True")
    return True

def ChromaSpecPayloadClassFactory( command_id, name, variables, sizes, repeat=None ):
  log.info("command_id=%d name=%s variables=%s sizes=%s repeat=%s", command_id, name, variables, sizes, repeat)
  if repeat:
    klass = type( str(name), (ChromaSpecRepeatPayload,), {
      'command_id'   : int(command_id),
      'name'         : name,
      'variables'    : variables,
      'sizes'        : sizes,
      'repeat'       : repeat,
    } )
  else:
    klass = type( str(name), (ChromaSpecPayload,), {
      'command_id'   : int(command_id),
      'name'         : name,
      'variables'    : variables,
      'sizes'        : sizes,
    } )
  log.info("return %s", klass)
  return klass
  
import re
_payloadSize = { 'B' : 1, 'H': 2, 'L': 4, 's': 1 }
# NOTE: currently unused but possibly useful for later if there are
#       more mixed-format packets, like repeating multi-blobs of data
def _chunkPayload( payload, chopsize ):
  log.debug("payload=%s chopsize=%d", payload, chopsize)
  chopped = 0
  payrest = payload
  paychop = b''
  while chopped < chopsize and payrest:
    ns = re.match('([0-9]+)s',payrest)
    log.debug("chopped=%d payrest=%s ns=%s", chopped, payrest, ns)
    if ns:
      n = int(ns.groups()[0])
      nlen = len(str(n))+1
      paychop += payrest[0:nlen]
      payrest  = payrest[nlen:]
      chopped += n
    else:
      paychop += payrest[0]
      payrest  = payrest[1:]
      chopped += _payloadSize.get(paychop)
  log.debug("return paychop=%s payrest=%s", paychop, payrest)
  return paychop, payrest
    
