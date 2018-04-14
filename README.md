
<img src="images/QISKit.gif">

***

THIS IS CURRENTLY STILL BE ORGANIZED. THE OLD VERSION IS IN THE OLD_TUTORIAL_FORMAT BUT WE WILL GET THIS DONE AS FAST AS WE CAN

# QISKit Tutorials

Welcome to the Quantum Information Software Kit ([QISKit](https://www.qiskit.org/) for short) tutorials! 

In this repository, we've put together a collection of Jupyter notebooks aimed at teaching people who want to use the QISKit for writing quantum computing programs and executing them on one of several backends (online quantum processors, online simulators, and local simulators). For the online quantum processors connects to the [IBM Q Systems](https://quantumexperience.ng.bluemix.net/qx/devices).

## Installation and Setup
Please refer to this [installation](INSTALL.md) for installing and setting up QISKit and tutorials on your own machine.

You can also run the tutorials online without installation on the [IBM Data Science Experience](https://datascience.ibm.com/) following the instructions in this [notebook](DSX.ipynb).

***

## Contents
We have organized the tutorials into three sections:

### 1. [Hello, Quantum World](hello_world/)
Since quantum computing is so new to most users, we want to find the best *Hello Quantum World* program and welcome submissions here. 

### 2. [Reference](reference/)<a id='reference'></a>
We've collected a core reference set of notebooks in this section. These notebooks demonstrate how to use QISKit and explore quantum information science, acting as a reference guide for QISKit. We will be keeping them up to date with QISKit updates. They are organized into the following topics:

#### 2.1 [Getting started with QISKit](reference/tools)
In this first topic, we introduce you to the basic features of QISKit.
        
#### 2.2 [Introduction to quantum information science](reference/qis)
The next set of notebooks shows how you can explore some simple concepts of quantum information science. 
    
####  2.3 [Understanding your quantum computer](reference/qcvv)
This set of notebooks describe a few of the techniques used to characterize, verify and validate quantum systems. 

####  2.4 [Working on approximate quantum computers](reference/approximate)
Universal fault tolerant quantum computers are still many years away, notebooks in this section describe a few of the things you can do with the approximate quantum computers we have today.

#### 2.5 [Examples of quantum algorithms](reference/algorithms)
This section contains notebooks describing the canonical quantum algorithms. 

####  2.6 [Having fun with quantum computers](reference/games)
Here we have a few examples of quantum games. Enjoy!

### 3. [Appendix](appendix)<a id='appendix'></a>
This is where the rest of the tutorials are. They are not guaranteed to work with the latest version of the QISKit, but we will do our best. 
***  

## Contributing
If you would like to contribute to the tutorials, there are a number of ways to get involved:

* **Issues**: Issues can be reported with GitHub [issue reporting](https://github.com/QISKit/qiskit-tutorial/issues) for this repository. Select `New issue` and fill in a descriptive title and provide as much detail as is needed for the issue to be reproduced.
* **Notebooks**: If you would like to contribute a notebook please create a [fork](https://help.github.com/articles/fork-a-repo/) of the repository from the `master` branch and create a [pull request](https://help.github.com/articles/about-pull-requests/) for your change. Note that new notebooks should be placed in the relevant part of the [Appendix](appendix) section. We will discuss in the [Slack channel](https://qiskit.slack.com/messages/C7SN3T90V) which of these should be in the [Reference](reference) section.

## Contributors
An alphabetical list of contributors can be found [here](CONTRIBUTORS.md). If you have contributed to these tutorials, please include your name there.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/QISKit/qiskit-tutorial/blob/master/LICENSE) file for details.
