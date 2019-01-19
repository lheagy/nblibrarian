"""
Tools for running nblibrarian from the command-line
"""

import argparse
from .librarian import Librarian


def main():
    """
    Command line tool for nblibrarian
    """

    parser = argparse.ArgumentParser(
        description="Synchronizes a collection of notebooks from a 'warehouse' "
        "repository to a local repository based on the inputs in a library-config.yml file."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print information about the files being downloaded",
    )
    parser.add_argument(
        "--config",
        nargs="?",
        default=None,
        help="name of the configuration file (e.g. library-config.yml)",
    )
    parser.add_argument(
        "--overwrite", nargs="?", default="False", help="overwrite exsisting conent?"
    )
    args = parser.parse_args()

    overwrite = False
    if args.overwrite.lower() == "true":
        overwrite = True

    # set up the librarian
    lib = Librarian(config_file=args.config, verbose=args.verbose)

    # download the environment and notebooks
    lib.download_requirements(overwrite=overwrite)
    lib.download_notebooks(overwrite=overwrite)
