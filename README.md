
# QISKit Tutorials
***

Welcome to the Quantum Information Software Kit ([QISKit](https://www.qiskit.org/) for short) tutorials! 

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use the [QISKit SDK](https://github.com/QISKit/qiskit-sdk-py) for writing quantum computing programs and executing them on one of several backends (online quantum processors, online simulators, and local simulators). For the online quantum processors, QISKit uses the [QISKit API](https://github.com/QISKit/qiskit-api-py) to connect to the [IBM Q Experience](https://quantumexperience.ng.bluemix.net/qx/experience).


## Contents
***

We have organised the tutorials into three sections:

### 1. [Hello World](/hello_world)
Since quantum computing is so new, we want to find the best *Hello Quantum World* program and welcome submissions here. 

### 2. [Reference](/reference)<a id='reference'></a>
We've collected a core reference set of notebooks in this section. These notebooks demonstrate how to use QISKit and explore quantum information science, acting as a reference guide for QISKit. We will be keep them up to date with [QISKit SDK](https://github.com/QISKit/qiskit-sdk-py) updates. They are organized into the following topics:

#### 2.1 [Getting started with QISKit](/reference/tools)
In this first topic, we introduce you to the basic features of QISKit. More tutorials covering QISKit features can be found in [here](#appendix_tools) and developer documentation can be found [here](https://www.qiskit.org/documentation/).
  * Getting started
  * Working with different backends
  * Using different gates
  * Visualisation of quantum states
        
#### 2.2 [Introduction to quantum information science](/reference/qis)
The next set of notebooks shows how you can explore some simple concepts of quantum information science. More tutorials on other quantum information science concepts can be found [here](#appendix_qis)
  * [Superposition and entanglement](/reference/qis/superposition_and_entanglement.ipynb) - this tutorial shows you how to make simple quantum states on one and two qubits, and demonstrates concepts such as quantum superpositions and entanglement.
  * [Entanglement revisited](/reference/qis/entanglement_revisited.ipynb) - this tutorial delves deeper into quantum entanglement, looking at the CHSH inequality and Mermin's test.
  * [Quantum teleportation and superdense coding](reference/qis/teleportation_superdensecoding.ipynb) - this tutorial introduces two simple quantum communication protocols, based on the quantum entanglement. 
    
####  2.3 [Understanding your quantum computer](/reference/qcvv)
  * Relaxation and decoherence
  * Quantum tomography
  * Random Benchmarking

####  2.4 [Working an approximate quantum quantum computers](/reference/approximate)
  * Variational Quantum Eigensolver
  * Small error correcting codes
  * Error mitigation

#### 2.5 [Examples of quantum algorithms](/reference/algorithms)
  * [Deutsch–Jozsa algorithm](reference/algorithms/deustch_josza.ipynb)
  * [Bernstein-Vazirani algorithm](reference/algorithms/bernstein_vazirani.ipynb)
  * [Phase estimation](reference/algorithms/iterative_phase_estimation_algorithm.ipynb)
  * Simon's algorithm
  * Grover's algorithm
  * Shor's algorithm

####  2.6 [Having fun with quantum computers](/reference/games)
  * Battleships

### 3. [Appendix](/appendix)<a id='appendix'></a>
This is where the rest of the tutorials are. They are not guaranteed to work with the latest version of the QISKit SDK. They are organised into various topics:
  1. Advanced QISKit features<a id='appendix_tools'></a>
  2. More on quantum information science<a id='appendix_qis'></a>
  3. Further quantum algorithms and applications<a id='appendix_algorithms'></a>
  4. Everything else<a id='appendix_other'></a>

## Installation and Setup

### 1. Install the QISKit SDK

### 2. Install Jupyter

### 3. Get the tutorials

### 4. Explore the tutorials

Start Jupyter with the ``README`` notebook:

    jupyter notebook README.ipynb


## Contributing
If you would like to contribute to the tutorials, there are a number of ways to get involved:

* **Issues**: Issues can be reported with GitHub [issue reporting](https://github.com/QISKit/qiskit-tutorial/issues) for this repository. Select `New issue` and fill in a descriptive title and provide as much detail as is needed for the issue to be reproduced.
* **Notebooks**: If you would like to contribute a notebook please create a [fork](https://help.github.com/articles/fork-a-repo/) of the repository from the `master` branch and create a [pull request](https://help.github.com/articles/about-pull-requests/) for your change. Note that new notebooks should be placed in the relevant part of the [Appendix](/appendix) section. We will discuss in the [Slack channel](https://qiskit.slack.com/messages/C7SN3T90V) which of these should be in the [Reference](/reference) section.

Note that edits to this ``README`` should be made to the Jupyter notebook file ``(README.ipynb)`` and then the following command run to create the markdown file ``(README.md)`` for GitHub:

    jupyter nbconvert --to markdown README.ipynb

## Contributors
An alphabetical list of contributors can be found [here](CONTRIBUTORS.md). If you have contributed to these tutorials, please include your name there.

## Licence
This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/QISKit/qiskit-tutorial/blob/master/LICENSE) file for details.
