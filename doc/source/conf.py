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
sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'chromaspeclib'
copyright = '2020, Chromation Inc'
author = 'Sean Cusack'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinx.ext.autodoc', 
'sphinx.ext.coverage', 
'sphinx.ext.napoleon',
'm2r',
#'recommonmark'
]

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
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

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
  app.connect('autodoc-skip-member', skip_payload_attributes)

napoleon_numpy_docstring = True

