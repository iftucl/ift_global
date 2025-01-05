# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import date


project = 'ift_global'
copyright = f'{date.today().year}, UCL - Institute for Finance & Technology'
author = 'Luca Cocconcelli'
release = '0.1.0'

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, '../../../ift_global'))
sys.path.insert(0, target_dir)


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_css_files = [
    'css/custom.css',
]
html_theme = 'pydata_sphinx_theme'

html_logo = '_static/ift_global_banner.png'
# html_favicon = '_static/favicon.ico'

# The suffix of source filenames.
source_suffix = '.rst'

# The main toctree document.
master_doc = 'index'
default_colours = {"main": "#8a1047"}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    "sphinx_design",
    "sphinx-pydantic",
    ]

templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/tests/*"]

html_sidebars = {
    "index": ["search-button-field"],
    "**": ["search-button-field", "sidebar-nav-bs"]
}


language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#html_css_files = ["styles.css",]

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

html_title = f"{project} Manual"

autosummary_generate = True

html_context = {
   # ...
   "default_mode": "dark"
}