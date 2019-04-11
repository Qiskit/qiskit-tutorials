# Advanced Quantum Information Science with Qiskit Terra

This folder hosts notebooks on advanced topics of Quantum Information Science, note that all of them may not work with the latest version of qiskit. 

Now that you have seen that quantum superposition and entanglement are important features in quantum computing and information,
we will see how they can be used to obtain quantum advantages, as below.

* [Random Number Generation](random_number_generation.ipynb): demonstrate how to generate random numbers using a quantum computer.

* [Quantum Random Access Coding](single-qubit_quantum_random_access_coding.ipynb): show quantum advantages with one qubit that cannot be achieved with a single classical bit. The two-qubit version is also available [here](two-qubit_state_quantum_random_access_coding.ipynb).

* [Vaidman Detection Test](vaidman_detection_test.ipynb): show how to exploit probability computation between classical and quantum devices. Quantum computing works on probability amplitudes (instead of probability in classical), which is shown can mean either dead or alive! The ability to operate on probability amplitudes is also the basis of [the Grover search algorithm](../../algorithms/grover_algorithm.ipynb).

* [Quantum Fourier Transform](fourier_transform.ipynb): part of the [Shor's factoring algorithm](../../algorithms/shor_algorithm.ipynb) and an important block for extracting periodicity structures in many quantum algorithms.

* [Multi-Qubit W State Systems](Multi-Qubit_W_States_with_Tomography.ipynb): show an evidence that a customized circuit can be more efficient than the standard/generic one.

* [Topological Quantum Walk](topological_quantum_walk.ipynb): an example of applying quantum mechanics for random walk, which is a powerful tool in many classical randomized algorithms.

* [Wigner Functions](wigner_functions.ipynb): show how to create a quasiprobability density function (corresponding to probability density function in classical statistics) from density matrices.

* [Entangled Measurement](entangled_measurement.ipynb): show that entanglement can also be defined over quantum measurements just like over quantum states. And likewise, an equivalent inequality to test the existence of entangled measurement can also be derived just like the Bell/CHSH inequalities for the quantum states.

* [Quantum Finite Automata](comparing_classical_and_quantum_finite_automata.ipynb): show an example when quantum finite automata can be exponentially more efficient that its classical counterpart.

* [Quantum Pseudo-Telepathy](quantum_magic_square.ipynb): show that gambling with parties sharing quantum entanglement can be a headache as they can trick you proving something impossible with classical statistics.

* [The Structure of the Clifford Group](Clifford_Group.ipynb): 
This notebook describes the structure of the Clifford group, 
which consists quantum operators that can be efficiently 
simulated (in polynomial time) using a classical computer.
In addition, the Clifford group is used for Randomized Benchmarking.

* [Quantum Walk](quantum_walk.ipynb):an example of quantum walk on circle graph with 2^N(N: number of qubits) lattice points. Quantum walker moves around circle in accordance with unitary coin(In this example Hadamard).  This quantum walk is simpler than topological quantum walk(above one).
## Contributing

We welcome more examples in this folder, in particular, experimenting with the latest results in quantum information science.
