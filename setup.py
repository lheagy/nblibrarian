#!/usr/bin/env python

"""nblibrarian

Tools for maintaining a library of Jupyter notebooks that are sourced
from a "warehouse" of notebooks (a github repository)
"""

from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Natural Language :: English",
]

with open("README.rst") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

setup(
    name="nblibrarian",
    version="0.0.2",
    packages=find_packages(exclude=["docs/*", "tests/*"]),
    install_requires=["requests", "pyyaml"],
    author="Lindsey Heagy",
    author_email="lindseyheagy@gmail.com",
    description="nblibrarian: a utility for fetching notebooks from a source repository",
    long_description=LONG_DESCRIPTION,
    license="3-clause BSD",
    keywords="jupyter notebooks",
    url="http://github.com/lheagy/nblibrarian",
    download_url="http://github.com/lheagy/nblibrarian",
    classifiers=CLASSIFIERS,
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    entry_points={"console_scripts": ["nblibrarian = nblibrarian.command_line:main"]},
)
