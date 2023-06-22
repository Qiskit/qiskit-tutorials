# Qiskit Tutorials

[![License](https://img.shields.io/github/license/Qiskit/qiskit-tutorials.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)

> :warning: **This repository will be soon archived**: The content in this repository [is being moved to other locations](https://github.com/Qiskit/qiskit-tutorials/issues/1473). If you have issues or PR, consider submitting the to their new location. 

| previous location | new location | tracking issue/PR |
| --------  | -------- |  -------- |
|  [Circuit Basics](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits/01_circuit_basics.ipynb) <br/> [Getting started with Qiskit](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits/1_getting_started_with_qiskit.ipynb) | TBD | https://github.com/Qiskit/qiskit-terra/issues/10315 |
| [Qiskit Visualizations](https://qiskit.org/documentation/tutorials/circuits/2_plotting_data_in_qiskit.html) | https://qiskit.org/documentation/apidoc/visualization.html | https://github.com/Qiskit/qiskit-terra/issues/8567 |
| [Summary of Quantum Operations](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits/3_summary_of_quantum_operations.ipynb) | https://qiskit.org/documentation/apidoc/circuit_library.html | https://github.com/Qiskit/qiskit-terra/pull/7354 |
| [Advanced Circuits](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/01_advanced_circuits.ipynb) | | |
| [Advanced Circuits - Operators](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/02_operators_overview.ipynb) | | |
| [Advanced Circuits - Visualization](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/03_advanced_circuit_visualization.ipynb) | TBD | https://github.com/Qiskit/qiskit-terra/pull/8624 |
| [Advanced Circuits - Transpiler](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/04_transpiler_passes_and_passmanager.ipynb) |  | |
| [Advanced Circuits - Pulse gates](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/05_pulse_gates.ipynb) |  | |
| [Advanced Circuits - Building Pulse Schedules](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/06_building_pulse_schedules.ipynb) |  | |
| [Advanced Circuits - Using the Scheduler](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/07_pulse_scheduler.ipynb) |  | |
| [Advanced Circuits - Obtaining information about backend](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/circuits_advanced/08_gathering_system_information.ipynb) |  | |
|  [Simulators](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/1_aer_provider.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/1_aer_provider.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Device backend noise model simulations](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/2_device_noise_simulation.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/2_device_noise_simulation.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Building Noise Models](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/3_building_noise_models.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/3_building_noise_models.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Applying noise to custom unitary gates](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/4_custom_gate_noise.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/4_custom_gate_noise.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Noise Transformation](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/5_noise_transformation.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/5_noise_transformation.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Extended Stabilizer Simulator](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/6_extended_stabilizer_tutorial.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/6_extended_stabilizer_tutorial.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
|  [Matrix product state simulation method](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/simulators/7_matrix_product_state_method.ipynb) | https://github.com/Qiskit/qiskit-aer/blob/main/docs/tutorials/7_matrix_product_state_method.ipynb | https://github.com/Qiskit/qiskit-aer/pull/1768 |
| [An Introduction to Algorithms in Qiskit](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/algorithms/01_algorithms_introduction.ipynb) | | |

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
