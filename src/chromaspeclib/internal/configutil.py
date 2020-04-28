
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from chromaspeclib        import CHROMASPEC_ROOTDIR
from chromaspeclib.logger import CHROMASPEC_LOGGER_JSON as log
import os, sys

def findConfig(filename):
  log.info("filename=%s", filename)
  developer = os.path.join(CHROMASPEC_ROOTDIR, "cfg", filename)
  installed = os.path.join(sys.prefix, "share", "chromaspeclib", "cfg", filename)
  local     = os.path.join(".", filename)
  found     = None
  if(  os.access(developer, os.R_OK)): found = developer;
  elif(os.access(installed, os.R_OK)): found = installed;
  elif(os.access(local,     os.R_OK)): found = local;
  else: raise Exception("Cannot find config file %s"%(filename))
  return found

