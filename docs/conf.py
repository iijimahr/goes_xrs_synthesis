# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

project = "goes_xrs_synthesis"
author = "Haruhisa Iijima"
copyright = "2026, Haruhisa Iijima"

extensions = [
    "sphinx.ext.autodoc",  # Generate HTML files from docstrings
    "sphinx.ext.napoleon",  # Enable Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
]
templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
