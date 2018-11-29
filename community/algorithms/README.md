# Quantum Algorithms

This folder holds notebooks explaining textbook quantum algorithms. The notebooks contain mathematical details on the computational steps within the algorithms to guide you into standard techniques in quantum algorithms. If you are just interested in using them as sub procedures and want to avoid the evil details, please go to [the aqua folder](../aqua/).

Most of the textbook quantum algorithms here are to be used with fault-tolerant quantum devices, which unfortunately are non-existent today. So, they are unlikely fit for the near-term quantum devices. Nevertheless, they are essential to show the power of quantum algorithms.

## Contents

There are two important ingredients in designing quantum algorithms: **quantum superposition** and **quantum entanglement**.
Most algorithms use both quantum superposition and entanglement to obtain quantum advantages. You are expected to understand those two concepts from notebooks in [terra](../terra), especially, quantum [superposition](../terra/qis_intro/superposition.ipynb) and [entanglement](../terra/qis_intro/entanglement_introduction.ipynb).

* [Bernstein-Vazirani](bernstein_vazirani.ipynb) algorithm: who says one must have quantum entanglement for quantum advantages? This notebook presents how to solve the well-known algorithm without using the CNOT gates (for creating entanglement between qubits). Quantum superposition alone can give you quantum speedup!

* [Deutsch-Jozsa](deutsch_jozsa.ipynb) algorithm: help determine if a Boolean function is balanced or constant with a single quantum query. This is one of the first examples demonstrating the power of quantum algorithms against deterministic classical ones.

* [Grover search](grover_algorithm.ipynb) algorithm: help you find a needle in a haystack faster with quantum operations. The notebook shows how to solve a combinatorial problem naively with the Grover search. But, please notice that most of combinatorial problems have structures which can allow fast classical algorithms. For example, it is unlikely one can obtain quantum advantage by simply applying the Grover search to look for the best possible solution among all possible ones by brute-force quantum search. You have been warned!


You probably have heard many times that near-term quantum computers will be used in tandem with classical computers: quantum computers are used for attacking special subproblems whose solutions are then processed by classical computers. These types of hybrid algorithms have been known for quite some time, as below.

* [Simon](simon_algorithm.ipynb) algorithm: help you determine if a function is one-to-one or two-to-one with resources exponentially more efficient that any classical algorithm. It uses classical computers for post-processing the output of quantum computation.

* [Shor](shor_algorithm.ipynb) algorithm: help you break the [RSA encryption](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) by factorizing an integer into its prime factors. Here, you will see the power of quantum Fourier transform to efficiently extract periodicity structures.

* [Iterative Phase Estimation](iterative_phase_estimation_algorithm.ipynb) algorithm: to efficiently compute eigenvalues of unitary matrices. The quantum technique for this is famously known as quantum phase estimation. Its iterative version allows you to estimate with smaller number of qubits, and thus is more tailored to near-term quantum devices.      


## What's next

Now that you have witnessed the power of quantum computing on perfect quantum devices, you may want to see how quantum algorithms perform on noisy quantum devices by [examples in qiskit-aqua](../aqua/index.ipynb).
