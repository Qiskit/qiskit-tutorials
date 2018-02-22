
# QISKit Tutorials
***

Welcome to the Quantum Information Software Kit ([QISKit](https://www.qiskit.org/) for short) tutorials! 

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use the [QISKit SDK](https://github.com/QISKit/qiskit-sdk-py) for writing quantum computing programs and executing them on one of several backends (online quantum processors, online simulators, and local simulators). For the online quantum processors, QISKit uses the [QISKit API](https://github.com/QISKit/qiskit-api-py) to connect to the [IBM Q Systems](https://quantumexperience.ng.bluemix.net/qx/experience).

## Installation and Setup
Please refer to [this note](INSTALL.ipynb) for installation and how to submit new tutorials by using github functionalities. 

You can also use a webhosted Jupyter notebook environment with [IBM DSX](https://github.com/QISKit/qiskit-tutorial/wiki/Running-Quantum-Program-on-IBM-DSx) as shown [here](running_on_IBM_DSX.ipynb).  


## Contents
***
We have organised the tutorials into three sections:

### 1. [Hello, Quantum World](hello_world/)
Since quantum computing is so new to most users, we want to find the best *Hello Quantum World* program and welcome submissions here. 

### 2. [Reference](reference/)<a id='reference'></a>
We've collected a core reference set of notebooks in this section. These notebooks demonstrate how to use QISKit and explore quantum information science, acting as a reference guide for QISKit. We will be keeping them up to date with [QISKit SDK](https://github.com/QISKit/qiskit-sdk-py) updates. They are organized into the following topics:

#### 2.1 [Getting started with QISKit](reference/tools)
In this first topic, we introduce you to the basic features of QISKit. More tutorials covering QISKit features can be found in [here](#appendix_tools) and developer documentation can be found [here](https://www.qiskit.org/documentation/).
  * [Getting started](reference/tools/getting_started.ipynb) - how to use QISKit.
  * [Working with different backends](reference/tools/working_with_backends.ipynb) - running quantum program on different backends.
  * [Using different gates](reference/tools/quantum_gates_and_linear_algebra.ipynb) - list of gates in QISKit and their linear algebra.
  * [Visualisation of quantum states](reference/tools/visualizing_quantum_state.ipynb) -  illustrates the different tools we have for visualizing a quantum state.
        
#### 2.2 [Introduction to quantum information science](reference/qis)
The next set of notebooks shows how you can explore some simple concepts of quantum information science. More tutorials on other quantum information science concepts can be found [here](#appendix_qis)
  * [Superposition and entanglement](reference/qis/superposition_and_entanglement.ipynb) - this tutorial shows you how to make simple quantum states on one and two qubits, and demonstrates concepts such as quantum superpositions and entanglement.
  * [Entanglement revisited](reference/qis/entanglement_revisited.ipynb) - this tutorial delves deeper into quantum entanglement, looking at the CHSH inequality and Mermin's test.
  * [Quantum teleportation and superdense coding](reference/qis/teleportation_superdensecoding.ipynb) - this tutorial introduces two simple quantum communication protocols, based on the quantum entanglement. 
    
####  2.3 [Understanding your quantum computer](reference/qcvv)
  * [Relaxation and decoherence](reference/qcvv/relaxation_and_decoherence.ipynb) - a simple notebook showing how to measure coherence.
  * [Quantum state tomography](reference/qcvv/state_tomography.ipynb) - how to identify quantum states
  * [Quantum process tomography](reference/qcvv/process_tomography.ipynb) - how to perform quantum state reconstruction
  * Random Benchmarking

####  2.4 [Working on approximate quantum computers](reference/approximate)
  * [Variational Quantum Eigensolver](reference/approximate/quantum_chemistry.ipynb) - how to perform quantum chemistry 
  * Small error correcting codes
  * Error mitigation

#### 2.5 [Examples of quantum algorithms](reference/algorithms)
  * [Deutsch–Jozsa algorithm](reference/algorithms/deutsch_josza.ipynb) - a deterministic quantum algorithm that outperforms the corresponding classical algorithm.
  * [Bernstein-Vazirani algorithm](reference/algorithms/bernstein_vazirani.ipynb) - a quantum algorithm that outperforms classical probabilistic algorithms.
  * [Phase estimation](reference/algorithms/iterative_phase_estimation_algorithm.ipynb) - a quantum algorithm to extract eigenvalues of unknown unitary operator.
  * Simon's algorithm
  * [Grover's algorithm](reference/algorithms/grover_algorithm.py) - a python program of Grover search on 3 qubits. 
  * Shor's algorithm

####  2.6 [Having fun with quantum computers](reference/games)
  * [Battleships](reference/games/battleships_with_partial_NOT_gates.ipynb) - a version of Battleships made to run on ibmqx3. The unique properties of single qubit operations are used to implement the game mechanics, with the destruction of a ship corresponding to rotation from 0 to 1.
  * [Which is the counterfeit coin?](reference/games/quantum_counterfeit_coin_problem.ipynb) - can you solve the counterfeit coin riddle? You are given a quantum computer and quantum beam balance, and your task is to find a counterfeit coin hidden in a set of coins. Armed with the knowledge of the Bernstein-Vazirani algorithm, you can easily find the counterfeit coin using the beam balance only once.

### 3. [Appendix](appendix)<a id='appendix'></a>
This is where the rest of the tutorials are. They are not guaranteed to work with the latest version of the QISKit SDK. They are organised into various topics:
  1. Advanced QISKit features<a id='appendix_tools'></a>
  2. More on quantum information science<a id='appendix_qis'></a>
  3. Further quantum algorithms and applications<a id='appendix_algorithms'></a>
  4. Everything else<a id='appendix_other'></a>


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


