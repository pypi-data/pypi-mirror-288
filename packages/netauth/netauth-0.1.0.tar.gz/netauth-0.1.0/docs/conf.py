# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os, sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'netauth'
copyright = '2024, classabbyamp'
author = 'classabbyamp'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'enum_tools.autoenum',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_member_order = 'bysource'
autodoc_type_aliases = {
    'KVDict': 'dict[str, list[str]]',
}

sys.path.insert(0, os.path.abspath('..'))

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_logo = "https://www.netauth.org/img/NetAuthLock.png"
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 2,
}
