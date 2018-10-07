
<img src="images/qiskit-heading.gif" >

***

# Guide for Installation and Setup

## 1. Download the Qiskit Tutorials

**Get the tutorials**<BR>

For the full experience, you can start by [downloading](https://github.com/Qiskit/qiskit-tutorial/archive/master.zip) the tutorials. Unzip the archive in the directory of your choice (this is the recommend way). Alternatively, the more advanced user may choose to use `git`. If you have `git` installed, run

```
git clone https://github.com/Qiskit/qiskit-tutorial.git
```

To properly view and run the tutorials, you will need to install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html).

If you need to install `git` follow the instructions [here](https://help.github.com/articles/set-up-git/).


## 2. Install Qiskit, Qiskit Aqua and Qiskit Aqua Chemistry

At least [Python 3.5 or later](https://www.python.org/downloads/) is required to install and use Qiskit. If you have multiple Python versions installed (and particularly if the command `python --version` returns an incompatble version), you will need to ensure that your versions are [managed correctly](https://conda.io/docs/user-guide/tasks/manage-python.html). This can be done using the `QISKitenv.yml` file, as detailed below.

When there are no issues with dependencies, Qiskit can be simply installed using

```
pip install qiskit qiskit-aqua qiskit-aqua-chemistry
```

Or, pre-installed qiskit can be updated using

```
pip install -U qiskit qiskit-aqua qiskit-aqua-chemistry
```

However, in case of issues with dependencies, we recommend the following installation procedure:

1. **Install [conda](https://conda.io/docs/index.html)**

2. **Create conda environment for Qiskit and install packages** (with the accompanying `environment.yml` file)

```
cd qiskit-tutorial
conda env create -f environment.yml
```

If you have already created `environment`, you can upgrade it by running

```
conda env update -f environment.yml
```


## 3. Configure your IBMQ provider

-  Create an `IBM Q <https://quantumexperience.ng.bluemix.net>`__ account if
   you haven't already done so
-  Get an API token from the IBM Q website under “My
   Account” > “Advanced”
-  The API token can be used by

```python
    from qiskit import IBMQ

    IBMQ.enable_account('MY_API_TOKEN')
```



## 4. Explore the tutorials

**Activate the environment**<BR>
For MacOS and Linux, run:

```
source activate Qiskitenv
```

For Windows, run:

```
activate Qiskitenv
```
**Note for conda users**<BR>t
You need to be sure that you have installed the right Jupyter Kernel, because in the last conda version it's not installed by default.

```
python -m ipykernel install --user --name Qiskitenv --display-name "Python (Qiskitenv)"
```

**Start Jupyter with the index notebook**<BR>

```
jupyter notebook index.ipynb
```

## 5. Visualizing Circuits
You can visualize your quantum circuits directly from Qiskit. To get publication-quality images, Qiskit plots circuits using LaTeX, which means you will need to install some pre-requisite software. These include the `pdflatex` compiler for rendering latex documents, and the Poppler library for converting PDF to image. In the future, we will provide ways of plotting circuits without relying on Latex.

On Linux:

- Install [MiKTeX](https://miktex.org/download#unx)
- Install Poppler:
	- Run: ```apt-get install -y poppler-utils```

On MacOS:

- Install [MiKTeX](https://miktex.org/download).
- Install Poppler:
	- Run:```brew install poppler```

On Windows:

- Install [MiKTeX](https://miktex.org/download).
- Install Poppler:
	- Download the [latest binary](http://blog.alivate.com.au/wp-content/uploads/2017/01/poppler-0.51_x86.7z).
	- Extract the downloaded `.7z` file into user directory:
`c:\Users\<user_name>\`.
Note: You will need to have the [7zip software](https://www.7-zip.org/download.html) for this.
	- Add to PATH:
		- Right click on "This PC" -> Properties -> Advanced System Settings -> Environment Variables
		- Add `C:\Users\<user_name>\poppler-0.51\bin` to the user's path.
