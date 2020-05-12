#!/usr/bin/env python

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

"""
Example Usage
=============

Capture one frame once
----------------------
chromaspec_cmdline.py captureframe

Capture a frame 50 times with 2 seconds inbetween
-------------------------------------------------
chromaspec_cmdline.py captureframe -r 50 -w 2

Capture a frame and print results in csv
----------------------------------------
chromaspec_cmdline.py captureframe -c

Set the binning to true, gain to 100, and row_bitmap to 010101 (0x15)
---------------------------------------------------------------------
chromaspec_cmdline.py setsensorconfig binning=1 gain=100 row_bitmap=0x15

Connect to a specific COM4 port
-------------------------------
chromaspec_cmdline.py -f COM4 ...

Connect to a specific /dev/com123 file
--------------------------------------
chromaspec_cmdline.py -f /dev/com123 ...

Connect to emulator instead of hardware
---------------------------------------
chromaspec_cmdline.py -e ...

"""

def main():
  import subprocess, sys
  subprocess.call(["python", "-m", "chromaspeclib.cmdline"] + sys.argv[1:])
  
if __name__ == "__main__":
  main()
