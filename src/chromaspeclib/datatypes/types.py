from chromaspeclib.internal.jsonparse import globalizeJsonFile
from chromaspeclib                    import CHROMASPEC_ROOTDIR
import os

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

