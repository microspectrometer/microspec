#!/usr/bin/env python

import sys
import argparse
parser = argparse.ArgumentParser(
  description="Create software instance of Chromation hardware for use with testing access software")
parser.add_argument("-v", "--verbose", help="Print verbose trace",                action="count", default=0)
parser.add_argument("-d", "--debug",   help="Internal debugging",                 action="count", default=0)
parser.add_argument("-p", "--print",   help="Print socket to connect to",         action="count", default=0)
parser.add_argument("-t", "--timeout", help="Timeout in (partial float) seconds", nargs=1,        default=[0],
                                                                                  action="store", type=float)
parser.add_argument("-s", "--spawn",   help="Spawn socat instance?",              action="count", default=False)
parser.add_argument("-f", "--file",    help="File to use as a pipe - default create anew and print location", 
                                                                                                  default=None)
args = parser.parse_args()

from chromaspeclib.internal.emulator import ChromaSpecEmulator
from chromaspeclib.internal.stream   import ChromaSpecEmulatedStream
from chromaspeclib.internal.logger   import debug
import logging

log = logging.getLogger("chromaspec_emulator")
if args.verbose or args.debug: 
  debug( args.debug>0 )
  log.setLevel( logging.DEBUG )

serial   = ChromaSpecEmulatedStream(hardware=args.file, timeout=args.timeout[0], socat=args.spawn, fork=False)
emulator = ChromaSpecEmulator()

if args.file is None or args.print:
  print("%s"%(serial.software))
  # Note: necessary so that the emulator object that spawns this program and waits for some input
  # on stdout definitely gets data, otherwise it gets stuck in the buffer and never triggers select:
  sys.stdout.flush() 

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

