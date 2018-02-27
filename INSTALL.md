<img src="images/QISKit.gif" >

***

# Installation and Setup

## 1. Install the [QISKit SDK](https://github.com/QISKit/qiskit-sdk-py)

If the SDK has not already been installed, follow the installation
instructions in the README file in the [QISKit SDK
repository](https://github.com/QISKit/qiskit-sdk-py).

Briefly, the steps are:

1.  Install [conda](https://conda.io/docs/index.html)
2.  Create conda environment for QISKit:
```
conda create -y -n QISKitenv python=3 pip scipy
```
3.  Activate the environment
    -   MacOS, Linux: `source activate QISKitenv`
    -   Windows: `activate QISKitenv`
4.  Install qiskit:
Please note that the **master** branch of the tutorials, is intented
to be used with the **master** branch (development version) of the
SDK. As a result, for using it you need to clone the SDK repository
(and periodically update it) via:
```
    git clone https://github.com/QISKit/qiskit-sdk-py.git
```
If you do not need access to the most recent features, please
consider using the `stable` version of the tutorials instead. When
using the **stable** branch of the tutorials, the stable version of
the SDK can be installed via:
```
pip install qiskit
```
5.  Setup API token
> 1.  Create an [IBM Quantum Experience
>     Experience](https://quantumexperience.ng.bluemix.net) account
>     if you haven't already done so
> 2.  Get an API token from the Quantum Experience website under "My
>     Account" &gt; "Personal Access Token"
> 3.  You will insert your API token in a file called Qconfig.py in
>     the qiskit-tutorial directory. The contents of the file should
>     look like,
>
>     > ```
>     > APItoken = 'my token from the Quantum Experience'
>     > config = {'url': 'https://quantumexperience.ng.bluemix.net/api'}
>     >
>     > if 'APItoken' not in locals():
>     >     raise Exception('Please set up your access token. See Qconfig.py.')
>     > ```
>

## 2. Install [Jupyter](http://jupyter.readthedocs.io/en/latest/install.html)

After the previous step you should have a `QISKitenv`
[conda](https://conda.io/docs/index.html) environment and your API token
setup. In a terminal window make sure you are in the QISKitenv conda
environment,

> -   MacOS, Linux: `source activate QISKitenv`
> -   Windows: `activate QISKitenv`

Then install jupyter with,

```
conda install jupyter
```

## 3. Get the tutorials

Using `git` to clone the SDK repository is the easiest way to keep up
with the latest changes or to contribute to the tutorials.

```
git clone https://github.com/QISKit/qiskit-tutorial.git
```

Alternatively it is also possible to just download the source files in a
ZIP archive. For the ZIP file download, select the desired branch from
the `Branch` drop-down button on the GitHub page. Usually this would be
the highest revision branch available or `master` if you want the latest
development version. Select the green `Clone or download` button then
`Download ZIP` to get the source file archive.

##. Explore the tutorials

In a terminal window copy or link your Qconfig.py file from step (1)
into this directory.

-   Linux, macOS: `cp /path/to/Qconfig.py qiskit-tutorial`
-   Windows: `copy \path\to\Qconfig.py qiskit-tutorial`

Go to the `qiskit-tutorial` directory.

```
cd qiskit-tutorial
```

Start Jupyter with the README notebook.

```
jupyter notebook README.ipynb
```