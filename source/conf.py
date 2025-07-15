# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DICOM Store SCP for AWS HealthImaging'
copyright = '2025, Man Machine Interface, Inc.'
author = 'Tatsuhiko Arai'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Internationalization options --------------------------------------------
language = 'en'
locale_dirs = ['../locale/']
gettext_compact = False

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# -- HTML theme options ------------------------------------------------------
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,

    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- PDF output options ------------------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',
    'printindex': '\\footnotesize\\raggedright\\printindex',
}

latex_documents = [
    ('index', 'dicom-store-scp.tex', 'DICOM Store SCP for AWS HealthImaging Documentation',
     'AWS Marketplace', 'manual'),
]
