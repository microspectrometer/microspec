
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

"""
cmdline
=======

Foo bar baz

"""

from chromaspeclib.simple            import ChromaSpecSimpleInterface
from chromaspeclib.logger            import debug, CHROMASPEC_LOGGER as log
from chromaspeclib.datatypes.command import CHROMASPEC_COMMAND_NAME as commands
from chromaspeclib.datatypes.types   import CHROMASPEC_GLOBAL       as constants
import time, datetime, sys

cmdname = dict([ [s[7:].lower(), s[7:]] for s    in commands.keys() ])
cstname = dict([ [s    .lower(), v    ] for s, v in constants.items() ])

def get_command(c):
  return cmdname.get(c.lower())

def get_constant(c):
  return cstname.get(c.lower(), c)

def print_format(csv, response):
  current_time = datetime.datetime.now().strftime("%Y-%m-%dT%T.%f%z")
  if response is None:
    print("%s,%s"%(current_time,None))
  elif csv:
    print("%s,%s"%(current_time,response.csv()))
  else:
    print("%s,%s"%(current_time,str(response)))

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description="Command line interface for ChromaSpecLib")
  parser.add_argument("-d", "--debug",    help="Internal debugging trace",           action="count", default=0    )
  parser.add_argument("-v", "--verbose",  help="Verbose trace",                      action="count", default=0    )
  parser.add_argument("-t", "--timeout",  help="Timeout (seconds)",                  type=float,     default=0.1  )
  parser.add_argument("-r", "--repeat",   help="Repeat N times, 1=once, 0=forever",  type=int,       default=1    )
  parser.add_argument("-w", "--wait",     help="Wait inbetween repeats (seconds)",   type=float,     default=1.0  )
  parser.add_argument("-e", "--emulator", help="Spawn emulator and connect to that", action="count", default=0    )
  parser.add_argument("-f", "--file",     help="File/socket/device to connect to, "+
                                               "default=auto-detect hardware",                       default=None )
  parser.add_argument("-c", "--csv",      help="Print-format: 'default' or 'csv'",   action="count", default=0    )
  parser.add_argument("-i", "--ignore",   help="Ignore argument",                                                 )
  parser.add_argument("command",          help="Command to send",                                                 )
  parser.add_argument("arguments",        help="Key=value pairs for command",        nargs="*",      default=[]   )
  args = parser.parse_args()
  
  from chromaspeclib.internal.stream import ChromaSpecEmulatedStream
  from chromaspeclib.logger          import debug
  if args.debug or args.verbose: 
    debug(args.debug>0)

  timeout = args.timeout

  si = None
  if args.emulator:
    log.info("Starting emulation process...")
    hardware = ChromaSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    software = ChromaSpecSimpleInterface(device=hardware.software, timeout=timeout)
    log.info("Connecting to emulation")
    si       = software
  elif args.file:
    log.info("Connecting to device '%s'", args.file)
    si       = ChromaSpecSimpleInterface(device=args.file, timeout=timeout)
  else:
    log.info("Connecting to default hardware")
    si       = ChromaSpecSimpleInterface(timeout=timeout)

  try:
    getcmd  = get_command(args.command)
    command = getcmd[0].lower() + getcmd[1:]
  except:
    log.critical("Command '%s' not found!", args.command)
    sys.exit(1)

  try:
    kwargs  = dict([ [s.split("=")[0],get_constant(s.split("=")[1])]  for s in args.arguments ])
  except:
    log.critical("Error parsing arguments '%s'", str(args.arguments))
    sys.exit(1)

  i = 0
  while (True if args.repeat < 0 else i < args.repeat):
    log.info("Executing command %s(%s)", command, kwargs)
    try:
      reply = getattr(si, command)(**kwargs)
      print_format(args.csv, reply)
    except Exception as e:
      log.error(e)
      print_format(args.csv, None)
    i += 1
    if (True if args.repeat < 0 else i < args.repeat):
      if args.repeat > 0:
        log.info("%d calls remain", args.repeat - i + 1)
      log.info("Waiting %f seconds...", args.wait)
      time.sleep(args.wait)

