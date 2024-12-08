# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AnimeScraper'
copyright = '2024, Muhammad MuQiT'
author = 'Muhammad MuQiT'
release = "1.1.0"
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google-style docstrings
    'sphinx.ext.viewcode',  # To include links to the source code
    'sphinx.ext.autodoc.typehints',# Display type hints
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]
# Napoleon settings
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
# Autodoc default options
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'private-members': False,
    'special-members':  False,
}


autodoc_member_order = "bysource"

#autodoc_exclude_members = ['__init__']

templates_path = ['_templates']

exclude_patterns = [
    '_parse_anime_data.py',
    'tests/*',
    'async_malscraper.py',
    'sync_malscraper.py',
    '_cache_utils.py',
    'cli.py',
    'exceptions.py'
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


html_show_sourcelink = False


html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]

html_logo = "../assets/AnimeScraper.png"
html_favicon = "../assets/AnimeScraper.png"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "blue",
        "color-brand-content": "#CC3333",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/togashigreat/AnimeScraper",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}

