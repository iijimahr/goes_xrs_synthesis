project = "goes_xrs_synthesis"
author = "Haruhisa Iijima"
copyright = "2026, Haruhisa Iijima"

extensions = [
    "sphinx.ext.autodoc",  # Generate HTML files from docstrings
    "sphinx.ext.napoleon",  # Enable Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.doctest",  # Enable test code snippets
]
templates_path = ["_templates"]
exclude_patterns = []

# Autodoc settings
autodoc_typehints = "description"

html_theme = "bizstyle"
html_context = {
    "display_github": True,
    "github_user": "iijimahr",
    "github_repo": "goes_xrs_synthesis",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
