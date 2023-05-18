# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config


# -- Project information -----------------------------------------------------
project = 'Qiskit Tutorials'
copyright = '2020, Qiskit Development Team'  # pylint: disable=redefined-builtin
author = 'Qiskit Development Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '0.18.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.extlinks',
    'nbsphinx',
    "qiskit_sphinx_theme",
]
html_static_path = ['_static']
templates_path = ['_templates']

exclude_patterns = ['*.ipynb', '_build', 'legacy_tutorials',
                    '**.ipynb_checkpoints', '.tox']

nbsphinx_timeout = 300
nbsphinx_execute = 'always'
nbsphinx_widgets_path = ""
html_sourcelink_suffix = ""
nbsphinx_thumbnails = {"**": "_static/no_image.png"}

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
language = "en"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'colorful'

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined), e.g. for
# py:function directives.
add_module_names = False

# -- Options for HTML output -------------------------------------------------

html_theme = 'qiskit_sphinx_theme'

html_logo = 'images/logo.png'
html_last_updated_fmt = '%Y/%m/%d'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
}

autoclass_content = 'both'
