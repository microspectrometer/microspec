#!/usr/bin/env python
import sys
import argparse
parser = argparse.ArgumentParser(description="Create software instance of Chromation hardware for use with testing access software")
parser.add_argument("-v", "--verbose", help="Print verbose trace", action="store_true")
parser.add_argument("-d", "--debug",   help="Turn on additional debugging", nargs=1)
parser.add_argument("socket",          help="File to use as a pipe - default create anew and print location", nargs=1)
args = parser.parse_args()

from chromaspeclib.internal.emulator import ChromaSpecEmulator
emulator = ChromaSpecEmulator()

import logging
from chromaspeclib.internal.logger import CHROMASPEC_LOGGER, CHROMASPEC_LOGGER_INTERNAL, CHROMASPEC_LOGGER_STREAM
CHROMASPEC_LOGGER.setLevel(logging.DEBUG)
#CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.DEBUG)
CHROMASPEC_LOGGER_STREAM.setLevel(logging.DEBUG)

#TODO: handle default no socket given
from chromaspeclib.internal.stream import ChromaSpecSerialIOStream
serial = ChromaSpecSerialIOStream(device=args.socket[0], timeout=1)
while True:
  command = serial.receiveCommand()
  if not command:
    continue
  print("got command=%s",command)
  reply = emulator.process(command)
  if reply:
    print("processed reply=%s",reply)
    for packet in reply:
      serial.sendReply(packet)
  else:
    print("processed no reply")

