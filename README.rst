.. image:: images/QISKit-c.gif
    :align: center

QISKit - Jupyter Notebooks
==========================

This repository contains Jupyter notebooks demonstrating quantum
computing using QISKit, the open source quantum information software
developer's toolkit. They provide an excellent way to learn,
contribute, and collaborate on topics in quantum computing.

Organization
------------
The notebooks are organized into several categories

1. Introduction to the tools
2. Exploring quantum information concepts
3. Verification tools for quantum information science
4. Applications of short-depth quantum circuits on quantum computers
5. Quantum games

For further information checkout out the Jupyter notebook index.ipynb
at the top of this repo.

Installation and setup
----------------------

1. Install the `QISKit SDK <https://github.com/QISKit/qiskit-sdk-py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the SDK has not already been installed, follow the installation
instructions in the README file in the
`QISKit SDK repository <https://github.com/QISKit/qiskit-sdk-py>`__.

Briefly, the steps are:

1. install `conda <https://conda.io/docs/index.html>`_
2. create conda environment for QISKit::

    conda create -y -n QISKitenv python=3 pip scipy

3. activate the environment

   - MacOS, Linux: ``source activate QISKitenv``
   - Windows: ``activate QISKitenv``

3. install qiskit:

   Please note that the **master** branch of the tutorials, is intented to be
   used with the **master** branch (development version) of the SDK. As a
   result, for using it you need to clone the SDK repository (and periodically
   update it) via::

    git clone https://github.com/QISKit/qiskit-sdk-py.git

   If you do not need access to the most recent features, please consider using
   the ``stable`` version of the tutorials instead. When using the **stable**
   branch of the tutorials, the stable version of the SDK can be installed
   via::

   pip install qiskit

4. setup API token

    1. Create an
       `IBM Quantum Experience Experience <https://quantumexperience.ng.bluemix.net>`__
       account if you haven't already done so
    2. Get an API token from the Quantum Experience website under "My Account" > "Personal Access Token"
    3. You will insert your API token in a file called Qconfig.py in the qiskit-tutorial directory. The contents of the file should look like,

        .. code:: python

            APItoken = 'my token from the Quantum Experience'
            config = {'url': 'https://quantumexperience.ng.bluemix.net/api'}

            if 'APItoken' not in locals():
                raise Exception('Please set up your access token. See Qconfig.py.')

2. Install `Jupyter <http://jupyter.readthedocs.io/en/latest/install.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the previous step you should have a ``QISKitenv`` `conda
<https://conda.io/docs/index.html>`_ environment and your API token
setup. In a terminal window make sure you are in the QISKitenv conda
environment,

   - MacOS, Linux: ``source activate QISKitenv``
   - Windows: ``activate QISKitenv``

Then install jupyter with,

.. code:: sh

    conda install jupyter

3. Get the tutorials
~~~~~~~~~~~~~~~~~~~~

Using ``git`` to clone the SDK repository is the easiest way to
keep up with the latest changes or to contribute to the
tutorials. 

.. code:: sh

    git clone https://github.com/QISKit/qiskit-tutorial.git

Alternatively it is also possible to just download the source files in
a ZIP archive. For the ZIP file download, select the desired branch
from the ``Branch`` drop-down button on the GitHub page. Usually this
would be the highest revision branch available or ``master`` if you
want the latest development version. Select the green ``Clone or
download`` button then ``Download ZIP`` to get the source file
archive.

4. Explore the tutorials
~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal window copy or link your Qconfig.py file from step (1)
into this directory.

- Linux, macOS: ``cp /path/to/Qconfig.py qiskit-tutorial``
- Windows: ``copy \path\to\Qconfig.py qiskit-tutorial``

Go to the ``qiskit-tutorial`` directory.

.. code:: sh

    cd qiskit-tutorial

Start Jupyter with the index notebook.

.. code:: sh

    jupyter notebook index.ipynb


Contributing
------------

If you would like to contribute to the tutorials there are a number of
ways to get involved.

Issue Reporting
~~~~~~~~~~~~~~~

Issues can be reported with GitHub `issue reporting
<https://github.com/QISKit/qiskit-tutorial/issues>`__ for this
repo. Select ``New issue`` and fill in a descriptive title and provide
as much detail as is needed for the issue to be reproduced.

Please check the
`wiki <https://github.com/QISKit/qiskit-tutorial/wiki/QISKit-Tutorials>`__
for frequently asked questions and notes about common issues.

Notebooks
~~~~~~~~~

If you would like to contribute a notebook please create a `fork
<https://help.github.com/articles/fork-a-repo/>`__ of the repository
and create a `pull request
<https://help.github.com/articles/about-pull-requests/>`__ for your
change. To help with the review of your change it would be good to
include a detailed description of the contribution and a unit test
(e.g. using python's ``unittest`` framework). Notebooks being submitted to
the ``contrib`` directory will allow for the notebook to be part of
the repo while they are being vetted by the community.

Branch convention
~~~~~~~~~~~~~~~~~

Please note that this repository contains two branches:

- the ``stable`` branch contains tutorials that are meant to be compatible
  with the `latest stable release of
  QISKit <https://pypi.python.org/pypi/qiskit>`__.
- the ``master`` branch contains tutorials that are meant to be compatible
  with the `latest development version of
  QISKIT <https://github.com/QISKit/qiskit-sdk-py>`__. Please note that this
  branch includes features that might still not be ready for production, and
  requires that you install the SDK using git and keep up to date with the
  daily updates.

If you experience problems, please revise that the versions of the packages
installed on your system match the ones specified at the bottom of each
tutorial.

Using IBM DSx for your notebooks
---------------------------------
IBM Data Science Experience (DSx) is a platform where you can interactively 
run your quantum programs, collaborate and share your work with others. 

Among other things, it provides a ready-to-use environment to run Jupyter 
Python notebooks. For someone just getting started with QISkit, this is an 
excellent option. You can skip all the installation and environment creation 
steps on your computer, and instead use this web-hosted Jupyter notebook 
environment for running the Quantum programs. It also provides a platform 
where you can invite fellow researchers to collaborate on the notebooks 
you have developed or simply share your work within the community.

We have customized the example notebooks for you, so that you can 
directly run those using DSx. To get started, refer to this 
example: `1_introduction/running_on_IBM_DSX.ipynb`

See this `link
<https://github.com/QISKit/qiskit-tutorial/wiki/Running-Quantum-Program-on-IBM-DSx>`__ 
that gives step-by-step instructions on setting up an example notebook on DSx. 

Other QISKit projects
---------------------

-  `ibmqx backend
   information <https://github.com/QISKit/ibmqx-backend-information>`__
   Information about the different IBM Q experience backends.
-  `ibmqx user guide <https://github.com/QISKit/ibmqx-user-guides>`__
   The users guides for the IBM Q experience.
-  `OpenQasm <https://github.com/QISKit/openqasm>`__ Examples and tools
   for the OpenQASM intermediate representation.
-  `Python API <https://github.com/QISKit/qiskit-api-py>`__ API Client
   to use IBM Q experience in Python.
-  `Python SDK <https://github.com/QISKit/qiskit-sdk-py>`__ Software
   development kit for working with quantum programs in Python.

Contributors (alphabetically)
-----------------------------

Jerry Chow, Antonio Córcoles, Abigail Cross, Andrew Cross, Vincent Dwyer, Mark Everitt, Ismael Faro, Albert Frisch, Andreas Fuhrer, Jay M. Gambetta, Takashi Imamichi, Ali Javadi, Antonio Mezzacapo, Ramis Movassagh, Anna Phan, Rudy Raymond, Russell Rundle, Ninad Sathaye, Kristan Temme, Todd Tilma, Chris Wood, James Wootton.

In future updates anyone who contributes to the tutorials can include their name here.

License
-------

This project is licensed under the Apache License 2.0 - see the
`LICENSE <LICENSE>`__ file for details.
