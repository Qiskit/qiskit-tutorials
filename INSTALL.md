
<img src="images/QISKit.gif" >

***

# Beginner's Guide for Installation and Setup

## 1. Get the tutorials and install the QISKit SDK

1.  **Install [conda](https://conda.io/docs/index.html)**

2.  **Get the tutorials**<BR>
    The easiest way is to have `git` installed as described [here](https://help.github.com/articles/set-up-git/).
    If you have git installed, run
```
git clone https://github.com/QISKit/qiskit-tutorial.git
```
    If you just want to run the tutorials without `git`, you can [download tutorials](https://github.com/QISKit/qiskit-tutorial/archive/stable.zip). Unzip the archive in the directory of your choice.  
    
3. **Create conda environment for QISKit and install packages** (with the accompanied `qiskit-simple.yml` file)
```
 cd qiskit-tutorial
 conda env create -f qiskit-simple.yml
```   

4. **Activate the environment**<BR>
    For MacOS and Linux, run:
    ```
    source activate QISKitenv
    ```
    For Windows, run:
    ```
    activate QISKitenv
    ```

5.  **Setup the API token**<BR>
    Create the `Qconfig.py` from the template provided at `Qconfig.py.template`. Follow A, B, and C steps below.  
> 1.  Create an [IBM Q Experience](https://quantumexperience.ng.bluemix.net) account
>     if you haven't already done so
> 2.  Get an API token from the IBM Q Experience website under "My
>     Account" &gt; "Advanced" &gt; "API Token"
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
    

## 2. Explore the tutorials


Start Jupyter with the index notebook.
```
    jupyter notebook README.ipynb
```
