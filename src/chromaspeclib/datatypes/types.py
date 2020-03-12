# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from chromaspeclib.internal.jsonparse import globalizeJsonFile
from chromaspeclib                    import CHROMASPEC_ROOTDIR
import os, sys

CHROMASPEC_GLOBAL = \
  globalizeJsonFile(
    os.path.join(
      CHROMASPEC_ROOTDIR,
      "cfg",
      "chromaspec.json"
    )
  )

globals().update([[k,v] for k,v in CHROMASPEC_GLOBAL.items()])

__all__ = list(CHROMASPEC_GLOBAL.keys())

__doc__ = "\n\n".join([""".. autoattribute:: chromaspeclib.datatypes.types.%s"""%(g) for g in __all__])
