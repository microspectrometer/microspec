#!/usr/bin/env python

import sys
import argparse
parser = argparse.ArgumentParser(
  description="Create software instance of Chromation hardware for use with testing access software")
parser.add_argument("-v", "--verbose", help="Print verbose trace, up to 3 times", action="count", default=0)
parser.add_argument("-d", "--debug",   help="Internal debugging, up to 3 times",  action="count", default=0)
parser.add_argument("-t", "--timeout", help="Timeout in (partial float) seconds", nargs=1,        default=0,
                                                                                  action="store", type=int)
parser.add_argument("socket",          help="File to use as a pipe - default create anew and print location", 
                                                                                  nargs="?",      default=None)
args = parser.parse_args()

from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.stream   import ChromaSpecSerialIOStream
from chromaspeclib.internal.logger   import CHROMASPEC_LOGGER, CHROMASPEC_LOGGER_INTERNAL, CHROMASPEC_LOGGER_STREAM
import logging
emulator = ChromaSpecEmulator()

def level(n):
  if n>=3: return logging.DEBUG
  if n>=2: return logging.INFO
  if n>=1: return logging.WARNING
  return logging.ERROR

log = logging.getLogger("chromaspec_emulator")
CHROMASPEC_LOGGER.setLevel(         level(args.verbose))
CHROMASPEC_LOGGER_INTERNAL.setLevel(level(args.debug  ))
log.setLevel(                       level(args.verbose))

if args.socket is None:
  import subprocess
  import tempfile
  import atexit
  import select
  import sys
  import os
  tempdir = tempfile.mkdtemp()
  hardware = os.path.join(tempdir, "chromation.hardware")
  software = os.path.join(tempdir, "chromation.software")
  #TODO: make this work for PC as well as MAC
  # Note: the -D is there to print something, anything, to stderr, so we can wait for it
  passthru = subprocess.Popen(["socat", "-D", "PTY,mode=666,link=%s"%(hardware),
                                              "PTY,mode=666,link=%s"%(software)],
                              stderr=subprocess.PIPE)
  r, w, x = select.select([passthru.stderr],[],[],1)
  #import pdb; pdb.set_trace();
  if not r:
    log.error("Cannot create socat process to mediate USB emulation!")
    sys.exit(1)
  serial = ChromaSpecSerialIOStream(device=hardware, timeout=args.timeout[0])
  def cleanup():
    log.warning("Cleanup: killing passthru process")
    passthru.kill()
    log.warning("Cleanup: removing temp directory %s"%(tempdir))
    os.rmdir(tempdir)
    log.warning("Cleanup: done")
  atexit.register(cleanup)
  print("Software connect to: %s"%(software))
else:
  serial = ChromaSpecSerialIOStream(device=args.socket[0], timeout=args.timeout[0])

while True:
  log.info("Waiting for command...")
  command = serial.receiveCommand()
  if not command:
    log.info("No command found")
    continue
  log.info("Received command %s"%(command))
  reply = emulator.process(command)
  if reply:
    log.info("Sending reply %s"%(reply))
    for packet in reply:
      serial.sendReply(packet)
  else:
    log.info("No reply to send")

