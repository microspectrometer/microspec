import logging

CHROMASPEC_LOG_FORMAT="%(asctime)-15s:%(filename)s:%(funcName)s:%(lineno)d: %(message)s"
logging.basicConfig(format=CHROMASPEC_LOG_FORMAT)

CHROMASPEC_LOGGER         =logging.getLogger("chromaspeclib")
CHROMASPEC_LOGGER_INTERNAL=logging.getLogger("chromaspeclib.internal")
CHROMASPEC_LOGGER_STREAM  =logging.getLogger("chromaspeclib.internal.stream")
CHROMASPEC_LOGGER_UTIL    =logging.getLogger("chromaspeclib.internal.util")
CHROMASPEC_LOGGER_PAYLOAD =logging.getLogger("chromaspeclib.internal.payload")
CHROMASPEC_LOGGER_JSON    =logging.getLogger("chromaspeclib.internal.json")
CHROMASPEC_LOGGER_DATA    =logging.getLogger("chromaspeclib.internal.data")

CHROMASPEC_LOGGER         .setLevel(logging.ERROR)
CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.ERROR)

def verbose(includeInternals=False):
  CHROMASPEC_LOGGER           .setLevel(logging.WARNING)
  if includeInternals:
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.WARNING)
  
def quiet(includeInternals=False):
  CHROMASPEC_LOGGER           .setLevel(logging.ERROR)
  if includeInternals:
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.ERROR)
  
def debug(includeInternals=False):
  CHROMASPEC_LOGGER           .setLevel(logging.DEBUG)
  if includeInternals:
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.DEBUG)
  
# Level uses:
# DEBUG:   Every substantial loop and branch
# INFO:    Every subroutine call and return
# WARNING: Minor errors that can usually be ignored
# ERROR:   Data format or API errors
# CRITIAL: Fatal errors like unopenable files or command line argument errors

# If you set the main logging level, everything will print, but if you set it
# just for one component, then just those and below will be produced

# One level per file isn't sufficient, as the reply and command data modules
# are spread out in multiple files

