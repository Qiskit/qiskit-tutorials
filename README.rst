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

2. Install `Jupyter <http://jupyter.readthedocs.io/en/latest/install.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the previous step you should have a ``QISKitenv`` `conda
<https://conda.io/docs/index.html>`_ environment and your API token
setup. In a terminal window make sure you are in the QISKitenv conda
environment,

.. code:: sh

					source activate QISKitenv

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

.. code:: sh

					cp /path/to/Qconfig.py qiskit-tutorial

Go to the ``qiskit-tutorial`` directory.

.. code:: sh

					cd qiskit-tutorial

Start Jupyter with the index notebook.

.. code:: sh

					jupyter notebook index.ibpynb
	 

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

Jerry Chow, Antonio Córcoles, Abigail Cross, Andrew Cross, Ismael Faro, Andreas Fuhrer, Jay M. Gambetta, Takashi Imamichi, Antonio Mezzacapo, Ramis Movassagh, Anna Phan, Rudy Raymond, Kristan Temme, Chris Wood, James Wootton

License
-------

This project is licensed under the Apache License 2.0 - see the
`LICENSE <LICENSE>`__ file for details.
