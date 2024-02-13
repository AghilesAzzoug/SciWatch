import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath("../src"))

project = "sci_watch"

copyright = "2024, Aghiles Azzoug"
author = "Aghiles Azzoug"
version = subprocess.run(["poetry", "version", "-s"], capture_output=True, text=True).stdout.rstrip()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

templates_path = ["_tempalates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autodoc_default_flags = ["members", "inherited-members"]
html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
html_theme_path = ["_themes"]

autosummary_generate = True
napoleon_numpy_docstring = True

source_suffix = [".rst", ".md"]
