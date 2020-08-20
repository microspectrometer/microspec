#!/usr/bin/env python

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

"""
Example Usage
=============

Capture one frame once
----------------------
microspec_cmdline.py captureframe

Capture a frame 50 times with 2 seconds inbetween
-------------------------------------------------
microspec_cmdline.py captureframe -r 50 -w 2

Capture a frame and print results in csv
----------------------------------------
microspec_cmdline.py captureframe -c

Set the binning to true, gain to 100, and row_bitmap to 010101 (0x15)
---------------------------------------------------------------------
microspec_cmdline.py setsensorconfig binning=1 gain=100 row_bitmap=0x15

Connect to a specific COM4 port
-------------------------------
microspec_cmdline.py -f COM4 ...

Connect to a specific /dev/com123 file
--------------------------------------
microspec_cmdline.py -f /dev/com123 ...

Connect to emulator instead of hardware
---------------------------------------
microspec_cmdline.py -e ...

"""

# noargdoc skips Sphinx post process for main-like functions
# sphinxcontrib.argdoc.ext.post_process_automodule() inserts a
# table listing an executable script's command-line arguments in
# :automodule: documentation, but this is causing the HTML build
# to fail.
# To see the error, delete these two lines, and in the Makefile
# run sphinx-build with option -vvv, like this:
# SPHINXOPTS    ?= -vvv
#
from sphinxcontrib.argdoc import noargdoc
@noargdoc
def main():
  import subprocess, sys
  subprocess.call(["python", "-m", "microspeclib.cmdline"] + sys.argv[1:])
  
if __name__ == "__main__":
  main()
