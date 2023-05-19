# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=invalid-name
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

"""
Sphinx documentation builder
"""

import os
import sys
# Set env flag so that we can doc functions that may otherwise not be loaded
# see for example interactive visualizations in qiskit.visualization.
os.environ['QISKIT_DOCS'] = 'TRUE'
if sys.platform == 'darwin':
    os.environ['QISKIT_IN_PARALLEL'] = 'TRUE'

# -- Project information -----------------------------------------------------
project = 'Qiskit Tutorials'
copyright = '2020, Qiskit Development Team'  # pylint: disable=redefined-builtin
author = 'Qiskit Development Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '0.18.0'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.extlinks',
    'nbsphinx',
    "qiskit_sphinx_theme",
]
html_static_path = ['_static']

html_sourcelink_suffix = ''
exclude_patterns = ['*.ipynb', '_build', 'legacy_tutorials',
                    '**.ipynb_checkpoints']

cell_timeout = int(os.getenv('QISKIT_CELL_TIMEOUT', 180))
nbsphinx_timeout = cell_timeout
nbsphinx_execute = 'always'
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'png', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

nbsphinx_thumbnails = {
}


nbsphinx_prolog = """
{% set docname = env.doc2path(env.docname, base=None) %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. note::
        This page was generated from `{{ docname }}`__.

        Run interactively in the `IBM Quantum lab <https://quantum-computing.ibm.com/jupyter/tutorial/{{ env.doc2path(env.docname, base=None)|replace("tutorials/", "") }}>`_.

    __ https://github.com/Qiskit/qiskit-tutorials/blob/master/{{ docname }}

"""


# If true, figures, tables and code-blocks are automatically numbered if they
# have a caption.
numfig = True

# A dictionary mapping 'figure', 'table', 'code-block' and 'section' to
# strings that are used for format of figure numbers. As a special character,
# %s will be replaced to figure number.
numfig_format = {
    'table': 'Table %s'
}
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'colorful'

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined), e.g. for
# py:function directives.
add_module_names = False


# -- Configuration for extlinks extension ------------------------------------
# Refer to https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'qiskit_sphinx_theme'  # use the theme in subdir 'theme'

html_logo = 'images/logo.png'
html_last_updated_fmt = '%Y/%m/%d'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#212121',
}

autoclass_content = 'both'
