#!/usr/bin/env python

"""
FOO
"""

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

def main():
  import subprocess, sys
  subprocess.call(["python", "-m", "chromaspeclib.cmdline"] + sys.argv)
  
if __name__ == "__main__":
  main()
