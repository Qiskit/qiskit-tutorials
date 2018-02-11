# QISKit Tutorials

Welcome to the QISKit tutorials. In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use QISKit for writing quantum computing experiments, programs, and applications.

## Contents
The tutorial notebooks are organised into three parts:

* [**Hello World**](/hello_world): Since quantum computing is so new, we want to find the best *Hello Quantum World* program and welcome submissions here.
* [**Reference**](/reference): These notebooks demonstrate how to use QISKit and explore quantum information science, acting as a reference book for QISKit. They will be kept up to date with QISKit SDK updates. They are organised into various topics:
  1. [Getting started with QISKit](/reference/tools)
    - Getting started
    - Working with backends (including compiling and running)
    - Using different gates
    - Visualisation of quantum states
  2. [Introduction to quantum information science](/reference/qis)
    - [Superposition and entanglement](/reference/qis/superposition_and_entanglement.ipynb)
    - [Entanglement revisited](/reference/qis/entanglement_revisited.ipynb)
    - [Quantum teleportation and superdense coding](reference/qis/teleportation_superdensecoding.ipynb)
  3. [Understanding your quantum computer](/reference/qcvv)
    - Relaxation and decoherence
    - Quantum tomography
    - Random Benchmarking
  4. [Working an approximate quantum quantum computers](/reference/approximate)
    - Variational Quantum Eigensolver
    - Small error correcting codes
    - Error mitigation
  5. [Examples of quantum algorithms](/reference/algorithms)
    - [Deutsch–Jozsa algorithm](reference/algorithms/deustch_josza.ipynb)
    - [Bernstein-Vazirani algorithm](reference/algorithms/bernstein_vazirani.ipynb)
    - [Phase estimation](reference/algorithms/iterative_phase_estimation_algorithm.ipynb)
    - Simon's algorithm
    - Grover's algorithm
    - Shor's algorithm
  6. [Having fun with quantum computers](/reference/games)
    - Battleships
    -
    -
* [**Appendix**](/appendix): This is where the rest of the tutorials are. They are not guaranteed to work with the latest version of the QISKit SDK. They are organised into various topics:
  1. Advanced QISKit features
  2. More on quantum information
  3. Further quantum algorithms and applications
  4. Everything else

## Installation and Setup

## Contributing
If you would like to contribute to the tutorials, there are a number of ways to get involved:

* **Issues**: Issues can be reported with GitHub [issue reporting](https://github.com/QISKit/qiskit-tutorial/issues) for this repository. Select `New issue` and fill in a descriptive title and provide as much detail as is needed for the issue to be reproduced.
* **Notebooks**: If you would like to contribute a notebook please create a [fork](https://help.github.com/articles/fork-a-repo/) of the repository from the `master` branch and create a [pull request](https://help.github.com/articles/about-pull-requests/) for your change. Note that new notebooks should be placed in the relevant section of the [Appendix](/appendix) section. We will discuss in the [Slack channel](https://qiskit.slack.com/messages/C7SN3T90V) which of these should be in the [Reference](/reference) section.

## Contributors
A list of contributors can be found [here](CONTRIBUTORS.md).


## Licence
This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/QISKit/qiskit-tutorial/blob/master/LICENSE) file for details.
