<img src="images/qiskit_header.png" >

# Qiskit Tutorials

[![License](https://img.shields.io/github/license/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)

Welcome to the [Qiskit](https://www.qiskit.org/) Tutorials!

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use Qiskit for writing quantum computing programs, and executing them on one of several backends (online quantum processors, online simulators, and local simulators). The online quantum processors are the [IBM Quantum](https://quantum-computing.ibm.com) systems.

For our community-contributed tutorials, please check out the [qiskit-community-tutorials](https://github.com/Qiskit/qiskit-community-tutorials) repository.

## Installation

The notebooks for these tutorials can be viewed here on GitHub.  However,  for the
full experience, you will want to interact with them.  The easiest way to do this
is by logging into the [IBM Quantum Experience](https://quantum-computing.ibm.com/), 
which lets you use Jupyter notebooks, including these tutorials, via the web.

Please refer to this [installation guide](INSTALL.md) for setting up Qiskit and
the tutorials on your own machine (this is the recommended way).

## Contents

To start seeing how Qiskit works, load up the [start_here.ipynb](start_here.ipynb) notebook
or view the tutorials in the [Qiskit documentation](https://qiskit.org/documentation/).

## Building documentation

In addition to serving up standalone notebooks, this repository also includes the infrastructure needed to build the tutorials into HTML documentation using [Sphinx](https://www.sphinx-doc.org/).  Along with the Qiskit dependencies, building the documentation requires the following:

```bash
pip install Sphinx
pip install sphinx-rtd-theme
pip install nbsphinx
```

## Contribution Guidelines

If you'd like to contribute to Qiskit IQX Tutorials, please take a look at our [contribution guidelines](.github/CONTRIBUTING.md). This project adheres to Qiskit's [code of conduct](.github/CODE_OF_CONDUCT.md). By participating, you are expect to uphold to this code.

We use [GitHub issues](https://github.com/Qiskit/qiskit-iqx-tutorials/issues) for tracking requests and bugs. Please use our [Slack](https://qiskit.slack.com) for discussion and simple questions. To join our Slack community, use the
[link](https://join.slack.com/t/qiskit/shared_invite/enQtODQ2NTIyOTgwMTQ3LTI0NzM2NzkzZjJhNDgzZjY5MTQzNDY3MGNiZGQzNTNkZTE4Nzg1MjMwMmFjY2UwZTgyNDlmYWQwYmZjMjE1ZTM).
For questions that are more suited for a forum, we use the Qiskit tag in the [Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/qiskit).

## Authors and Citation

Qiskit IQX Tutorials is the work of [many people](https://github.com/Qiskit/qiskit-iqx-tutorials/graphs/contributors) who contribute to the project at different levels. If you use Qiskit, please cite as per the included [BibTeX
file](https://github.com/Qiskit/qiskit/blob/master/Qiskit.bib).

## License

[Apache License 2.0](LICENSE)
