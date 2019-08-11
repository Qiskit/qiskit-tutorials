
<img src="images/qiskit-heading.gif" >

***

# Guide for Installation and Setup

## 1. Download the Qiskit Tutorials

**Get the tutorials**<BR>

For the full experience, you can start by downloading the latest release of the tutorials from [here](https://github.com/Qiskit/qiskit-tutorials/releases). Unzip the archive in the directory of your choice (this is the recommended way). 

To properly view and run the tutorials, you will need to install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html).

## 2. Install Qiskit, Qiskit Aqua and Qiskit Aqua Chemistry

At least [Python 3.5 or later](https://www.python.org/downloads/) is required to install and use Qiskit. If you have multiple Python versions installed (and particularly if the command `python --version` returns an incompatble version), you will need to ensure that your versions are [managed correctly](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python). This can be done using the `environment.yml` file, as detailed below.

When there are no issues with dependencies, Qiskit can be installed using

```
pip install qiskit
```

Or, pre-installed Qiskit can be updated using

```
pip install -U qiskit
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


## 3. Configure your IBM Q Provider

-  Create an [IBM Q](https://quantumexperience.ng.bluemix.net) account if
   you haven't already done so
-  Get an API token from the IBM Q website under “My
   Account” > “Advanced”
-  We are now going to add the necessary credentials to Qiskit. Take your token, here called `MY_API_TOKEN`, 
   and pass it to the `IBMQ.save_account()` function:

```python
    from qiskit import IBMQ

    IBMQ.save_account('MY_API_TOKEN')
```

-  Your credentials will be stored on disk. Once they are stored, at any point in the future you can load and use 
   them via:

```python
    from qiskit import IBMQ

    IBMQ.load_accounts()
```

-  For those who do not want to save their credentials to disk, please use

```python
    from qiskit import IBMQ

    IBMQ.enable_account('MY_API_TOKEN')
```

and the token will only be active for the session. 


## 4. Explore the Tutorials

**Activate the environment**<BR>
For MacOS and Linux, run:

```
source activate Qiskitenv
```

For Windows, run:

```
activate Qiskitenv
```
**Note for conda users**<BR>
Verify that you have installed the right Jupyter Kernel, because in the last conda version it's not installed by default.

```
python -m ipykernel install --user --name Qiskitenv --display-name "Python (Qiskitenv)"
```

**Start Jupyter with the index notebook**<BR>

```
jupyter notebook index.ipynb
```

## 5. [Optional] Visualizing Circuits with LaTeX
You can visualize your quantum circuits directly from Qiskit. Qiskit circuit drawers support text, LaTeX and matplotlib. The text and matplotlib version is entirely native to Python, and thus easy to use. The LaTeX version produces publication-quality circuit images, but relies on some pre-requisite software. These include the `pdflatex` compiler for rendering LaTeX documents, and the Poppler library for converting PDF to image. To get these:

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
