
<img src="images/qiskit-logo.gif" >

***

# Guide for Installation and Setup

## 1. Download the QISKit Tutorials

**Get the tutorials**<BR>

The easiest way is to [download](https://github.com/QISKit/qiskit-tutorial/archive/master.zip) the tutorials. Unzip the archive in the directory of your choice.

The more advanced user may choose to use `git`. If you have `git` installed, run

```
git clone https://github.com/QISKit/qiskit-tutorial.git
```

If you need to install `git` follow the instructions [here](https://help.github.com/articles/set-up-git/).


## 2. Install QISKit

The latest release version of QISKit should be the one installed.  The latest release can be installed using

```
pip install qiskit
```

**but we recommend the following**:


1. **Install [conda](https://conda.io/docs/index.html)**

2. **Create conda environment for QISKit and install packages** (with the accompanying `QISKitenv.yml` file)

```
cd qiskit-tutorial
conda env create -f QISKitenv.yml
```   

## 3. Setup the API Token

Create the `Qconfig.py` from the template provided at `Qconfig.py.template`. Follow the three steps below.  

1.  Create an [IBM Q Experience](https://quantumexperience.ng.bluemix.net) account
     if you haven't already done so
2.  Get an API token from the IBM Q Experience website under "My
     Account" &gt; "Advanced" &gt; "API Token"
3.  You will insert your API token in a file called Qconfig.py in
     the ```qiskit-tutorial``` directory. The contents of the file should
     look like:

```
APItoken = 'my token from the Quantum Experience'
config = {'url': 'https://quantumexperience.ng.bluemix.net/api'}

if 'APItoken' not in locals():
     raise Exception('Please set up your access token. See Qconfig.py.')
```



## 4. Explore the tutorials

**Activate the environment**<BR>
For MacOS and Linux, run:

```
source activate QISKitenv
```

For Windows, run:

```
activate QISKitenv
```
**Start Jupyter with the index notebook**<BR>

```
jupyter notebook index.ipynb
```
