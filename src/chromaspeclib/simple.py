from chromaspeclib.internal.data.command import CHROMASPEC_COMMAND_NAME
from chromaspeclib.expert import ChromaSpecExpertInterface

# The Simple interface doesn't retuire creating objects or doing any sending and waiting
# loops, instead it simply acts like a hardware object that you query for information

def generateFunction(command):
  cname = command.__name__
  name  = cname[7:8].lower()+cname[8:]
  def func(self, *args, **kwargs):
    return self.sendAndReceive(command(*args, **kwargs))
  return name, func

def generateDocstring(command):
  cname = command.__name__
  name  = cname[6:6].lower()+cname[7:]
  return "%s(%s)\n"%(name, ", ".join([c for c in command.variables if c != "command_id"]))

ChromaSpecSimpleInterface = type('ChromaSpecSimpleInterface',
                                 (ChromaSpecExpertInterface,),
                                 dict([generateFunction(command) for command in CHROMASPEC_COMMAND_NAME.values()]))
ChromaSpecSimpleInterface.__doc__ = "".join([generateDocstring(command) for command in CHROMASPEC_COMMAND_NAME.values()])
