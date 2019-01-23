"""
Tools for parsing a .jupyter-include file and assessing if a source file
meets those criteria or not
"""

import fnmatch
import re


def parse_jupyter_include(file=".jupyter-include"):
    """
    open a .jupyter-include file and parse the contents into a list
    """
    # open and read the contents of the .jupyter-include file
    with open(file, "r") as jupyter_include_file:
        include_criteria = jupyter_include_file.read()

    # remove lines that are commented out or empty
    include_criteria = include_criteria.split("\n")
    include_criteria = [
        c for c in include_criteria if not c.startswith("#") and c != ""
    ]

    return include_criteria


def include(source, include_criteria):
    """
    check if a file (`source`) should be included given the `include_criteria`
    """

    # fnmatch.translates enforces exact paths (i.e. nothing before and nothing after)
    # we want to be more flexible so I remove those constraints
    # (the first 3 characters and the last 3 characters)
    if any([re.search(fnmatch.translate(c)[4:-3], source) for c in include_criteria]):
        return True
    return False
