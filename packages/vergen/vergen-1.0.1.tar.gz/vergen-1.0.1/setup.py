from setuptools import setup, find_packages
from vergen.Application import Application

app = Application()

setup(
    name = app.name,
    version = app.version,
    packages = find_packages(),
    install_requires = [],
    entry_points = {
        "console_scripts": [
            "vergen=vergen.main:main"
        ]
    },
    author = "Shayan Eftekhari",
    author_email = "shayan.eftekhari@gmail.com",
    description = app.description,
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/wxShayan/vergen",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.8"
)
