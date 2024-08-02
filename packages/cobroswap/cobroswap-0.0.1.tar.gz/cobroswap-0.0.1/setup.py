from pathlib import Path
from setuptools import find_packages, setup

setup(
    name = "cobroswap",
    version = "0.0.1",
    author = "Alejo Prieto Dávalos",
    author_email = "alejoprietodavalos@gmail.com",
    packages = find_packages(),
    description = "Python wrapper for CobrosWap.",
    long_description = Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/cobroswap/",
    project_urls = {
        "Source": "https://github.com/AlejoPrietoDavalos/cobroswap/"
    },
    python_requires = ">=3.11",
    install_requires = [
        "requests>=2.32.0"
    ],
    include_package_data = True
)
