import os

__copyright__ = """Copyright 2020 Chromation, Inc"""
__license__   = """All Rights Reserved by Chromation, Inc"""

# NOTE: Sphinx ignores __init__.py files, so for generalized documentation,
#       please use pydoc, or the sphinx-generated documents in doc/build,
#       or the README.md file

# NOTE on CHROMASPEC_ROOTDIR
#
# It is specifically located in the __init__.py of the base chromaspeclib
# package, so that the ../ (src) ../ (chromaspec) directory can be found,
# so that, in turn, the cfg and other directories can be referenced
# programmatically and without relative references throughout the
# packages. The test system can find root package directories, but the
# runtime system has no standard for this, and we are avoiding utilizing
# a test system for runtime use.
#
# If chromaspeclib is in /foo/bar/chromaspec/src/chromaspeclib then
# CHROMASPEC_ROOTDIR will be /foo/bar/chromaspec

CHROMASPEC_ROOTDIR = os.path.realpath(
                       os.path.join(
                         os.path.dirname(__file__), # chromaspeclib
                         "..",                        # src
                         ".."                         # chromaspec
                       )
                     )

