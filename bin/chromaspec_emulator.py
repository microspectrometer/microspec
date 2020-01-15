#!/usr/bin/env python

import sys
import argparse
parser = argparse.ArgumentParser(
  description="Create software instance of Chromation hardware for use with testing access software")
parser.add_argument("-v", "--verbose", help="Print verbose trace",                action="count", default=0)
parser.add_argument("-d", "--debug",   help="Internal debugging",                 action="count", default=0)
parser.add_argument("-t", "--timeout", help="Timeout in (partial float) seconds", nargs=1,        default=0,
                                                                                  action="store", type=int)
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

serial   = ChromaSpecEmulatedStream(device=args.file, timeout=args.timeout[0])
emulator = ChromaSpecEmulator()

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

