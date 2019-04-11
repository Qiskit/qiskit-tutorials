# Quantum Games

Computer games have been around almost as long as computers. They begin with examples like [Nimrod](https://en.wikipedia.org/wiki/Nimrod_(computing)), [OXO](https://en.wikipedia.org/wiki/OXO) and [Spacewar!](https://en.wikipedia.org/wiki/Spacewar!), which were designed to help people learn about how early computers worked, and how to program them.

This is exactly what we'd like to replicate in this folder. Here you'll find basic examples of the tools and techniques of quantum programming, used to create the core of simple games. These all run in Jupyter notebooks, which are also used to explain the quantum programming behind the game.


## Contents

* [Hello Qiskit](Hello_Qiskit.ipynb) - Solve puzzles by creating simple Qiskit programs.

* [Battleships with partial NOT gates](battleships_with_partial_NOT_gates.ipynb) - Battleships implemented with single qubit rotations.

* [Quantum Counterfeit Coin Problem](quantum_counterfeit_coin_problem.ipynb) - A game based on finding a counterfeit coin, with a quantum strategy based on the Bernstein-Vazirani algorithm.

* [Quantum Tic-tac-toe](quantum_tic_tac_toe.ipynb) - Tic-tac-toe was one of the first games for a classical computer. Now we have a quantum version too!

* [Quantum Awesomeness](quantum_awesomeness.ipynb) - Puzzles that aim to give hands-on experience of a quantum device's most important features: number of qubits, connectivity and noise.

* [Random Terrain Generation](random_terrain_generation.ipynb) - A simple example of using quantum computers for the kind of procedural generation often used in games.

* [Quantum Animations](quantum_animations.ipynb) - A simple example of making pixel art animations with quantum computers.

## Contributing

Each game should have a Jupyter notebook in which the game is played, and in which the quantumness behind the game mechanic is explained.

If you are intimidated by the idea of explaining the quantum program, don't hesitate to contribute your game without it. Others will be happy to build on your work, and bring it in line with the required style.

To make even a simple command line game, you'll most likely need many lines of classical programming. This will handle the subtleties of input and output, and so not be directly relevant to someone learning quantum programming. You can therefore hide this away in a _.py_ file that can then be imported into your notebook. These files can be placed in the _game_engines_ folder. For example see _battleships_engine.py_ and its use in [Battleships with partial NOT gates](battleships_with_partial_NOT_gates.ipynb).

For more on how to contribute, see the main [README](../../README.md) for these tutorials.

