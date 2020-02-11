from chromaspeclib.expert            import ChromaSpecExpertInterface
from chromaspeclib.logger            import CHROMASPEC_LOGGER as log
from chromaspeclib.datatypes.command import CHROMASPEC_COMMAND_NAME

# The Simple interface doesn't retuire creating objects or doing any sending and waiting
# loops, instead it simply acts like a hardware object that you query for information

# The names of the methods are the names of the Command objects, but with the first letter
# lowercased. You can also look at the names of the commands in the JSON cfg file, or the
# pydoc for this class.

def _generateFunction(command):
  cname = command.__name__
  name  = cname[7:8].lower()+cname[8:]
  def func(self, *args, **kwargs):
    return self.sendAndReceive(command(*args, **kwargs))
  return name, func

def _generateDocstring(command):
  cname = command.__name__
  name  = cname[6:6].lower()+cname[7:]
  return "%s(%s)\n"%(name, ", ".join([c for c in command.variables if c != "command_id"]))

_ChromaSpecSimpleInterface = type('_ChromaSpecSimpleInterface',
                                 (ChromaSpecExpertInterface,),
                                 dict([_generateFunction(command) for command in CHROMASPEC_COMMAND_NAME.values()]))
_ChromaSpecSimpleInterface.__doc__ = "".join([_generateDocstring(command) for command in CHROMASPEC_COMMAND_NAME.values()])

class ChromaSpecSimpleInterface(_ChromaSpecSimpleInterface):
  def sendAndReceive(self, command, *args, **kwargs):
    # Simple interface ignores all other processing or in-progress calls, unlike Expert.
    # They are not compatible interfaces, as Expert can be continued after a failed read,
    # but Simple cannot. Do not intermix their usage.
    #
    # It can still get out of sync, but with enough of a wait, it will catch up next time
    log.info("command=%s args=%s kwargs=%s", command, args, kwargs)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.current_command = []
    reply = super().sendAndReceive(command, *args, **kwargs)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.current_command = []
    log.info("return %s", reply)
    return reply

__all__ = [ ChromaSpecSimpleInterface ]
