"""An example Qconfig file you can customize. Adapted from
example_Qconfig.py file provided in the QISKit tutorial files
provided by IBM on GitHub.

Set your configuration parameters to be imported into the notebooks.

The APIToken can be set as an environment variable in your shell session. For
example, in your ~/.bash_profile or ~/.bashrc add:

.. code-block:: bash

    export IBMQE_API="YOUR-API-TOKEN-HERE"

and restart your terminal session. This will add the ``$IBMQE_API`` as an
environment variable that can be accessed by the script.

Once imported, you can check the values have set using print:

.. code-block:: python

    import Qconfig
    print(Qconfig.APItoken, Qconfig.config['url'])

Alternately, one can hard-code their APIToken by copy-pasting it
directly into the assignment below.

"""
import os

# Uncomment this line if you have set the APIToken as a variable in your
# terminal session:
# APItoken = os.getenv("IBMQE_API")
# ^ change to match your variable name if needed

# Uncomment this line if you wish to hard-code your APIToken string:
# APItoken = "YOUR-API-TOKEN-HERE"
# ^ copy-paste full string into assignment

config = {"url": "https://quantumexperience.ng.bluemix.net/api"}

if APItoken is None:
    raise Exception("Please set up your access token. See Qconfig.py.")
