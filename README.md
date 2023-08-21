# Qiskit Tutorials

[![License](https://img.shields.io/github/license/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)

> :warning: **This repository is archived**: The content in this repository [was moved to other locations](https://github.com/Qiskit/qiskit-tutorials/issues/1473). If you have issues or PR, please submit them to their new location. 

* `algorithms` folder -> [`qiskit-algorithms`](https://qiskit.org/ecosystem/algorithms/tutorials/index.html) ([GitHub](https://github.com/qiskit-community/qiskit-algorithms/tree/main/docs/tutorials))
* `circuits` folder -> [Qiskit](https://qiskit.org/documentation/tutorials.html) ([GitHub](https://github.com/Qiskit/qiskit/tree/main/docs/tutorials/circuits))
* `circuits_advanced` folder -> [Qiskit](https://qiskit.org/documentation/tutorials.html) ([GitHub](https://github.com/Qiskit/qiskit/tree/main/docs/tutorials/circuits_advanced))
* `opflow` folder -> [Qiskit](https://qiskit.org/documentation/tutorials.html) ([GitHub](https://github.com/Qiskit/qiskit/tree/main/docs/tutorials/opflow))
* `simulators` folder -> [`qiskit-aer`](https://qiskit.org/ecosystem/aer/tutorials/index.html) ([GitHub](https://github.com/qiskit/qiskit-aer/tree/main/docs/tutorials))
* `textbook` folder -> removed in favor of https://www.qiskit.org/learn

## Contents

Welcome to the [Qiskit](https://www.qiskit.org/) Tutorials!

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use Qiskit for writing quantum computing programs, and executing them on one of several backends (online quantum processors, online simulators, and local simulators). The online quantum processors are the [IBM Quantum](https://quantum-computing.ibm.com) systems.

For our community-contributed tutorials, please check out the [qiskit-community-tutorials](https://github.com/Qiskit/qiskit-community-tutorials) repository.

## Contribution Guidelines

If you'd like to contribute to Qiskit Tutorials, please take a look at our [contribution guidelines](.github/CONTRIBUTING.md). This project adheres to Qiskit's [code of conduct](.github/CODE_OF_CONDUCT.md). By participating you are expected to uphold this code.

### Tutorial limitations
Because the tutorials are executed as part of the build process, and eventually turned into RST documentation, there are several limitations to be aware of:

  1. There is currently a three minute per cell execution time limit.  Cells that go over this limit will raise an exception.
  
  2. Tutorials cannot make calls to the IBM Quantum Experience, e.g. no `IBMQ.load_account()`.

  3. It is important to maintain strict header compliance.  All notebooks should start with, and contain only one, top level (h1) header:
  
      ```
      # I am a top level header
      ```
     
     Additionally, the nesting of headers should make sense:
     
      ```
      # I am a top level header
      
      ## I am a secondary header
      
      ### I am a tertiary header
      
      ## I am another secondary header
      
      ## I am another secondary header
      ```
     
   4. All math equations expressed using `$$ ... $$` need to be surrounded on top and bottom by white space.
   
   5.  In order for a tutorial to show up in the Qiskit documentation, after successful merging, an additional PR needs to be made in the [Qiskit meta-repo](https://github.com/Qiskit/qiskit) to trigger the rebuilding of the documentation.

### Adding a gallery image

To add a gallery image to a notebook, select a cell with an output image and add `nbsphinx-thumbnail` as a cell tag.  To see the cell tags go to: `View -> Cell Toolbar -> Tags` in the notebook menu.  Adding gallery images from images not generated inside of the notebooks themselves should be avoided if possible as this gets messy in the present build system.

## Building documentation

In addition to serving up standalone notebooks, this repository also includes the infrastructure needed to build the tutorials into HTML documentation using [Sphinx](https://www.sphinx-doc.org/).

We use [Tox](https://tox.wiki/en/latest/), which you will need to install globally (e.g. using [`pipx`](https://pypa.github.io/pipx/)).

1. Fork and clone the forked repository.
2. `tox -e docs`

Sometimes Sphinx's caching can get in a bad state. First, try running `tox -e docs-clean`, which will remove Sphinx's cache. If you are still having issues, try running `tox -e docs -r`. `-r` tells Tox to reinstall the dependencies.

## Authors and Citation

Qiskit Tutorials is the work of [many people](https://github.com/Qiskit/qiskit-tutorials/graphs/contributors) who contribute to the project at different levels. If you use Qiskit, please cite as per the included [BibTeX
file](https://github.com/Qiskit/qiskit-terra/blob/main/CITATION.bib).

## License

[Apache License 2.0](LICENSE)
