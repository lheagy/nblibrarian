import re


def parse_jupyter_include(file=".jupyter-include"):
    """
    open a .jupyter-include file and parse the contents into a list
    """
    # open and read the contents of the .jupyter-include file
    with open(file, "r") as file:
        include_criteria = file.read()

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
    if any([re.search(c, source) for c in include_criteria]):
        return True
    else:
        return False
