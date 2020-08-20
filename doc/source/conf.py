# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# Sean's paths. I don't think these do anything.
# sys.path.insert(0, os.path.abspath('../src'))
# sys.path.insert(1, os.path.abspath('../'))
#
# The following works to replace PYTHONPATH=../src
# It works both on my local build and the RTD build.
sys.path.insert(0, os.path.abspath('../../src'))
# The following works to replace PYTHONPATH=../tests (finds modules inside tests)
sys.path.insert(0, os.path.abspath('../../tests'))
# The following works to replace PYTHONPATH=../ (finds module tests and bin)
sys.path.insert(0, os.path.abspath('../../'))
# Proof that the above line makes bin.microspec_cmdline visible to import:
# import bin.microspec_cmdline
# print(bin.microspec_cmdline.__doc__)
# On local, I still need PYTHONPATH=../ make clean html
# The final fix to eliminate adjusting PYTHONPATH is to add the @noargdoc
# decorator to the two scripts with main-like functions:
# bin.microspec_cmdline
# bin.microspec_emulator

# -- Project information -----------------------------------------------------

project = 'microspec'
copyright = '2020, Chromation Inc'
author = 'Sean Cusack'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
"sphinx.ext.autodoc",
"sphinx.ext.coverage",
"sphinx.ext.napoleon",
# 'm2r', incompatible with Sphinx
#        see https://github.com/sphinx-doc/sphinx/issues/7420
"recommonmark", # replaces m2r
"sphinxcontrib.argdoc",
"sphinx_rtd_theme", # use the readthedocs theme
]

# Override readthedocs default: master_doc='contents.rst'
master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = '_static/CHROMATION.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static/']

# Autodoc options
autodoc_default_options = {
    'no-inherited-members': True,
    'undoc-members': False,
}

def skip_payload_attributes(app, what, name, obj, skip, options):
  if what == "class" and getattr(obj, "__qualname__", None) is None:
    # Skip attributes, this includes internal things like __doc__ but
    # also the class non-function attributes like led_num, because Sphinx
    # renders them horribly, so we might as well just leave it in the
    # class docstring instead
    #
    # NOTE: for some reason, even though led_num is UNDOCUMENTED, leaving
    # out undoc-members still insists on including them
    return True

def setup(app):
  # NOTE: This is a bit hacky, but sphinxcontrib-argdoc depends on a deprecated
  # call in Sphinx, so this is a workaround
  from sphinx.util import logging
  logger = logging.getLogger("sphinxcontrib.argdoc")
  app.debug2 = logger.debug

  # Connect to the class attribute skipping function
  app.connect('autodoc-skip-member', skip_payload_attributes)

napoleon_numpy_docstring = True

navigation_depth = 1

