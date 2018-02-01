"""An example Qconfig file you can customize.

Set your configuration parameters to be imported into the notebooks.

The APIToken can be set as an environment variable in your shell session. For
example, in your ~/.bash_profile or ~/.bashrc add:

.. code-block:: bash

    export IBMQE_API="your_secret_api_string"

and restart your terminal session. This will add the ``$IBMQE_API`` as an
environment variable that can be accessed by the script.

Once imported, you can check the values have set using print:

.. code-block:: python

    import Qconfig
    print(Qconfig.APItoken, Qconfig.config['url'])

"""
import os

APItoken = os.getenv("IBMQE_API")  # change to match your variable name if needed
config = {"url": "https://quantumexperience.ng.bluemix.net/api"}

if APItoken is None:
    raise Exception("Please set up your access token. See Qconfig.py.")
