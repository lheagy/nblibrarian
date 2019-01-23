.. image:: https://img.shields.io/pypi/v/nblibrarian.svg
    :target: https://pypi.python.org/pypi/nblibrarian
    :alt: Latest PyPI version
    
 .. image:: https://travis-ci.org/lheagy/nblibrarian.svg?branch=master
    :target: https://travis-ci.org/lheagy/nblibrarian
    :alt: TravisCI status
    
nblibrarian
===========

Tools for maintaining a library of Jupyter notebooks that are sourced
from a "warehouse" of notebooks (another github repository). 

Installing
----------

You can install nblibrarian from pypi

.. code:: shell

  pip install nblibrarian 
  
or from source

.. code:: shell

  git clone https://github.com/lheagy/nblibrarian
  cd nblibrarian
  pip install -e .
  

Configuring nblibrarian
-----------------------

There are two files that you need in order to configure `nblibrarian`:

- `.library-config.yml`
- `.jupyter-include`

.library-config.yml
^^^^^^^^^^^^^^^^^^^

The `.library-config.yml` file specifies details of the source repository and if you would like to include the `environment.yml` file and / or the `requirements.txt` file. (We recommend you download at least one of these). The structure of the `.library-config.yml` is as follows:

.. code:: yaml

  # information about the source library
  source:
    github:
      user: geoscixyz  # github username or organization
      repo: geosci-labs  # github repository
      branch: master  # [optional] branch to fetch material from 
      directory: notebooks  # [optional] directory where the notebooks are in the repository - including it will speed up the search for the desired notebooks

  # setup options for the library
  setup:
    environment: environment.yml  # [optional] include the environment.yml from the source
    requirements: requirements.txt  # [optional] include the requirements.txt file

.jupyter-include
^^^^^^^^^^^^^^^^

The `.jupyter-include` file describes which notebooks you would like included in your library. It follows the same 
syntax as a `.gitignore <https://git-scm.com/docs/gitignore>`_ file. 

.. code::

  # this is a comment

  # dc resistivity
  notebooks/dcip/DCIP_2D_Overburden_Pseudosections.ipynb  # you can specify the full path
  notebooks/dcip/DC_Building_Pseudosections  # also without the .ipynb extension
  DC_Cylinder_2D.ipynb  # or just specify the notebook name

  # em
  /em/EM_Pipeline.ipynb
  em/EM_ThreeLoopModel.ipynb
  em/*Sphere*.ipynb  # includes all notebooks in a directory called em with "Sphere" in the title

  # magnetics
  mag/*.ipynb  # includes all notebooks in the mag directory

  # inversion
  inversion  # includes notebooks in the inversion directory

Usage
-----

Once you have specified the `.library-config.yml` and the `.jupyter-include`, you can run nblibrarian from the command line to 
download the files you specified. 

.. code:: shell

  nblibrarian

There are also a few options, to run in `verbose` mode use

.. code:: shell

  nblibrarian -v 
  
If you ever want to update your library, you can always alter the `.jupyter-include` and re-run `nblibrarian`. By default, it will not overwrite your current notebooks. If you do want it to overwrite them, then run 

.. code:: shell

  nblibrarian --overwrite=True

If you would like to specify the path to the jupyter include and config files (for example if you put them in a different directory), then use

.. code:: shell

  nblibrarian --config=.library-config.yml --jupyter-include=.jupyter-include

Issues
------

If you run into any bugs, questions or problems using `nblibrarian`, please `create an issue <https://github.com/lheagy/nblibrarian/issues/new>`_ on github. 

License
-------

This work is Licensed under the `BSD 3-Clause License <LICENSE>`_. 
