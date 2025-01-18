.. _iftglobal-guides:

ift_global installation guides
===============================

.. contents:: Table of contents:
   :local:

Intro & important note
----------------------

.. warning::
    ift_global is in beta version and is not yet ready to be published on pypi.

Below we list the two main options to install the file.


From whl / tar files
--------------------

Wheel and tar file are built from Github Actions when a pull request is merged into the main branch.

You can select any of the `merged pull request and follow to the action triggered <https://github.com/iftucl/ift_global/actions/workflows/build.yml>`_ .

Each build artifact is available for download into the corresponding action.

From git using pip
------------------

Clone the repo to your local machine:

    git clone https://github.com/iftucl/ift_global.git

build the library locally:

    cd ift_global
    poetry run python -m pip install .


Using poetry
------------

If you manage your developments using poetry, you can add if_global as:

    poetry add git+https://github.com/iftucl/ift_global.git