"""
Main classes and functions for the nblibrarian.
"""

import os
import json
import yaml
import requests


from .jupyter_include import parse_jupyter_include, include

# global variables defining expectations and what we support
SUPPORTED_SOURCES = [
    "github"
]  #: List of source-code hosts that are currently supported by this package
EXPECTED_CONFIG = [
    "library-config",
    "nblibrary-config",
    "library_config",
    "nblibrary_config",
    "library",
    "nblibrary",
]  #: expected name of config file
EXPECTED_CONFIG_EXTENSION = ["yml", "yaml"]  #: extension of the config file


class Librarian:
    """
    Class for configuring and managing the library of notebooks.
    """

    def __init__(self, config_file=None, verbose=False):
        if config_file is not None:
            self.config_file = config_file  # go through the setter

        self.verbose = verbose

    @property
    def config_file(self):
        """
        name of the configuration file (e.g. library-config.yml)
        """
        if getattr(self, "_config_file", None) is None:
            files = [
                f
                for f in os.listdir()
                if any([f.endswith(ext) for ext in EXPECTED_CONFIG_EXTENSION])
            ]
            config_file = [f for f in files if f.split(".")[-2] in EXPECTED_CONFIG]

            if config_file == "" or len(config_file) > 1:
                raise Exception(
                    "Could not find library configuration file. Please specify "
                    "it by setting the 'config_file' property (e.g. "
                    "librarian.config_file = 'library-config.yml'"
                )

            self._config_file = config_file[0]

        return self._config_file

    @config_file.setter
    def config_file(self, value):
        if not any([value.endswith(ext) for ext in EXPECTED_CONFIG_EXTENSION]):
            raise Exception(
                f"The configuration file should have a .yaml or .yml file extension. "
                "The value you provided, {value}, does not."
            )
        else:
            self._config_file = value

    @property
    def config(self):
        """
        Dictionary containing the library configuration options
        """
        if getattr(self, "_config", None) is None:

            def check_config(config):
                if len(config["source"].keys()) > 1:
                    raise NotImplementedError(
                        "Currently, we only support data from a single source"
                    )

                for key in config["source"].keys():
                    if key not in SUPPORTED_SOURCES:
                        raise NotImplementedError(
                            f"Currently, we only support {SUPPORTED_SOURCES}. "
                            "The source you entered, in library-config.yml, {key} is "
                            "not supported"
                        )

            # load the yaml file
            with open(self.config_file, "r") as doc:
                config = yaml.load(doc)

            # check some of the config arguments
            check_config(config)

            # set the value
            self._config = config

        return self._config

    @property
    def source(self):
        """
        Dictionary containing the information about the source repository. It
        contains

        - user: github user for the source repository
        - repo: name of the repository
        - branch: branch that we will pull from
        """
        if getattr(self, "_source", None) is None:
            source = self.config["source"]["github"]
            user = source["user"]
            repo = source["repo"]

            # select either the provided branch or find the default branch on github
            if "branch" in source.keys():
                branch = source["branch"]
            else:
                req = requests.get(f"https://api.github.com/repos/{user}/{repo}")
                if req.ok:
                    branch = json.loads(req.content)["default_branch"]
                else:
                    raise Exception(
                        f"Could not find repo https://github.com/{user}/{repo}"
                    )
                source["branch"] = branch

            if self.verbose:
                print(
                    f"Source repository: https://github.com/{user}/{repo}/tree/{branch}"
                )

            self._source = source
        return self._source

    @property
    def content_url(self):
        """Source for the raw repository content on GitHub"""
        if getattr(self, "_content_url", None) is None:
            base = "https://raw.githubusercontent.com"
            self._content_url = f"{base}/{self.source['user']}/{self.source['repo']}/{self.source['branch']}"  # pylint: disable=line-too-long

        return self._content_url

    @property
    def notebook_list(self):
        """
        List of notebooks to be downloaded. This is based on the contents of
        the .jupyter-include file.
        """
        if getattr(self, "_notebook_list", None) is None:
            content = self.fetch_repo_contents()
            include_criteria = parse_jupyter_include()

            if "directory" in self.source.keys():
                of_interest = [
                    c
                    for c in content["tree"]
                    if c["path"].startswith(self.source["directory"])
                ]
            else:
                of_interest = content["tree"]

            of_interest = [
                item["path"] for item in of_interest if len(item["path"].split(".")) > 1
            ]

            self._notebook_list = [
                item for item in of_interest if include(item, include_criteria) is True
            ]

        return self._notebook_list

    def fetch_repo_contents(self):
        """
        Use the github API to fetch the contents of the source repository
        """
        url = f"https://api.github.com/repos/{self.source['user']}/{self.source['repo']}/git/trees/{self.source['branch']}?recursive=1"  # pylint: disable=line-too-long
        req = requests.get(url)

        if req.ok:
            content = json.loads(req.text)
        else:
            raise Exception(
                f"Could not fetch contents for https://github.com/{self.source['user']}/{self.source['repo']}/tree/{self.source['branch']}"  # pylint: disable=line-too-long
            )

        return content

    def download_requirements(self, overwrite=False):
        """Download the requirements and / or environment files from source library"""
        setup = self.config["setup"]

        for key in ["environment", "requirements"]:
            if key in setup.keys():
                url = self.content_url + f"/{setup[key]}"
                req = requests.get(url)

                if req.ok:
                    if overwrite is True or os.path.isfile(setup[key]) is False:
                        if self.verbose:
                            print(f"writing {setup[key]}")
                        with open(setup[key], "w") as file:
                            file.write(req.text)
                else:
                    raise Exception("Could not find url for {}".format(setup[key]))

    def download_notebooks(self, overwrite=False):
        """
        Download the desired notebooks
        """
        for notebook in self.notebook_list:
            # if the path doesn't exist, create it
            directory = os.path.sep.join(notebook.split("/")[:-1])

            if not os.path.isdir(directory):
                os.makedirs(directory)

            # download the notebook
            url = self.content_url + f"/{notebook}"
            req = requests.get(url)

            # make a windows friendly filename
            filename = os.path.sep.join(notebook.split("/"))

            if req.ok:
                if overwrite is True or os.path.isfile(filename) is False:
                    if self.verbose:
                        print(f"writing {filename}")
                    with open(filename, "w") as file:
                        file.write(req.text)

            else:
                raise Exception(f"Could not find {url}")
