from pathlib import Path
from setuptools import find_packages, setup

setup(
    name = "izienv",
    version = "0.1.0",
    author = "Alejo Prieto Dávalos",
    author_email = "alejoprietodavalos@gmail.com",
    packages = find_packages(),
    description = "Python package to handle multiple files with environment variables.",
    long_description = Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/izienv/",
    project_urls = {
        "Source": "https://github.com/AlejoPrietoDavalos/izienv/"
    },
    python_requires = ">=3.11",
    install_requires = [
        "python-dotenv>=1.0.1"
    ],
    include_package_data = True
)
