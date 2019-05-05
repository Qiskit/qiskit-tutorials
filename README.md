# Qiskit Tutorials

[![License](https://img.shields.io/github/license/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)[![](https://img.shields.io/github/release/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://github.com/Qiskit/qiskit-tutorials/releases)

Welcome to the [Qiskit](https://www.qiskit.org/) tutorials!

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use Qiskit for writing quantum computing programs, and executing them on one of several backends (online quantum processors, online simulators, and local simulators). The online quantum processors are the [IBM Q](https://quantumexperience.ng.bluemix.net/qx/devices) devices.

## Installation

The notebooks for these tutorials can be viewed here on GitHub. But for the full experience, you'll want to interact with them!

The easiest way to do this is using [the Binder image](https://mybinder.org/v2/gh/qiskit/qiskit-tutorials/master?filepath=index.ipynb), which lets you use the notebooks via the web. This means that you don't need to download or install anything, but it also means that you should not insert any private information into the notebooks (such as your API key). We recommend as pointed out in [issue #231](https://github.com/Qiskit/qiskit-tutorials/issues/231) that after you are done using mybinder that you regenerate your token.

Please refer to this [installation guide](INSTALL.md) for setting up Qiskit and the tutorials on your own machine (this is the recommended way).

## Contents

We have organized the tutorials into two sections:

### 1. [Qiskit notebooks](qiskit/)<a id='qiskit'></a>

We've collected a core reference set of notebooks in this section outlining the features of Qiskit. We will be keeping them up to date with the latest Qiskit version.  
- [Basics](qiskit/basics) is meant for those who are getting started.
- [Terra](qiskit/terra) is meant for those who want to study circuits.
- [Aer](qiskit/aer) is meant for those who want to simulate quantum circuits.
- [Ignis](qiskit/ignis) is meant for those who want to study noise.
- [Aqua](qiskit/aqua) is meant for those who want to develop applications on NISQ computers.
- [Jupyter](qiskit/jupyter) is meant to highlight some cool Juypter features.

### 2. [Community notebooks](community/)<a id='community'></a>

Teaching quantum computing and qiskit has many different paths of learning. We love our community, and we love the contributions so keep them coming. Because Qiskit is changing so much, at the moment we cant keep this updated, but there are some great notebooks in here. See:
- [Hello, Quantum World](community/hello_world/) learn from the community how to write your first quantum program.
- [Quantum Games](community/games/), learn quantum computing by having fun.
- [Quantum Information Science with Terra](community/terra/), learn about quantum information science with Qiskit Terra.
- [Textbook Quantum Algorithms](community/algorithms/), learn Qiskit from the textbook algorithms.
- [Quantum Algorithms](community/aqua/), learn about quantum algorithms for noisy near-term devices with Qiskit Aqua.
- [IBM Q Awards](community/awards/), learn from the great contributions to the [IBM Q Awards](https://qe-awards.mybluemix.net/), [Teach Me Qiskit 2018](community/awards/teach_me_qiskit_2018/index.ipynb) and [Teach Me Quantum 2018](community/awards/teach_me_quantum_2018/index.ipynb).

To go through the tutorials, load up the [index.ipynb](index.ipynb) notebook and start learning.

## Contribution Guidelines

If you'd like to contribute to Qiskit Tutorials, please take a look at our
[contribution guidelines](.github/CONTRIBUTING.md). This project adheres to Qiskit's [code of conduct](.github/CODE_OF_CONDUCT.md). By participating, you are expect to uphold to this code.

We use [GitHub issues](https://github.com/Qiskit/qiskit-tutorials/issues) for tracking requests and bugs. Please use our [slack](https://qiskit.slack.com) for discussion and simple questions. To join our Slack community use the [link](https://join.slack.com/t/qiskit/shared_invite/enQtNDc2NjUzMjE4Mzc0LTMwZmE0YTM4ZThiNGJmODkzN2Y2NTNlMDIwYWNjYzA2ZmM1YTRlZGQ3OGM0NjcwMjZkZGE0MTA4MGQ1ZTVmYzk). For questions that are more suited for a forum we use the Qiskit tag in the [Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/qiskit).

## Authors and Citation

Qiskit Tutorials is the work of [many people](https://github.com/Qiskit/qiskit-tutorials/graphs/contributors) who contribute
to the project at different levels. If you use Qiskit, please cite as per the included [BibTeX file](https://github.com/Qiskit/qiskit/blob/master/Qiskit.bib).

## License

[Apache License 2.0](LICENSE.txt)
