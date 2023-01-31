# Qiskit Tutorials

[![License](https://img.shields.io/github/license/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)

These tutorials are rendered as part of the:

### [>>Qiskit Documentation<<](https://qiskit.org/documentation/)


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


### Testing

This repo uses some automated tests to keep the content to a high standard.

- [Black](https://black.readthedocs.io/en/stable/) keeps formatting consistent, and can automatically fix some problems. To fix a notebook after editing it, run:

  ```bash
  nbqa black <path-to-notebook>
  ```

- [Pylint](https://github.com/PyCQA/pylint) checks for potential errors and enforces some coding styles. To test a notebook after editing it, run:

  ```bash
  nbqa pylint <path-to-notebook>
  ```

  You can disable Pylint rules for each notebook by adding a new code cell containing

  ```python
  # pylint: disable=<rule>
  ```
  and you can stop this cell appearing on the tutorials website by adding
  ```JSON
  {
    "nbsphinx": "hidden"
  }
  ```
  to the cell metadata.

To run these tests as they would in CI, run:

```bash
./tests/code.sh
```


## Building documentation

In addition to serving up standalone notebooks, this repository also includes the infrastructure needed to build the tutorials into HTML documentation using [Sphinx](https://www.sphinx-doc.org/).  Along with the Qiskit dependencies, building the documentation requires the following:

1. Fork and clone the forked repository. 
2. Create a new virtual environment and install pip:
```bash
conda create -n qiskit-tutorials-dev pip
```
3. Activate virtual environment:
```bash
conda activate qiskit-tutorials-dev
```
4. Install python dependencies in your new virtual environment:
```bash
pip install -r requirements-dev.txt
```
5. Install non-python dependencies:
```bash
conda install pandoc graphviz
```
6. Create a local build:
```bash
sphinx-build -b html . _build
```

## Authors and Citation

Qiskit Tutorials is the work of [many people](https://github.com/Qiskit/qiskit-tutorials/graphs/contributors) who contribute to the project at different levels. If you use Qiskit, please cite as per the included [BibTeX
file](https://github.com/Qiskit/qiskit/blob/master/Qiskit.bib).

## License

[Apache License 2.0](LICENSE)
