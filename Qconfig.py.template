# --------------------------------------------------------------------------------
# Before you can use the jobs API, you need to set up an access token.
# Log in to the Quantum Experience. Under "Account", generate a personal
# access token. There are two ways to set your API token
#
# METHOD-1:
#    Replace "None" value of variable APItoken with the quoted token string.
#    Uncomment the APItoken variable, and you will be ready to go.
#
# METHOD-2:
#   The APIToken can be set as an environment variable in your shell session. For
#   example, in your ~/.bash_profile or ~/.bashrc add:
#   .. code-block:: bash
#      export IBMQE_API="your_secret_api_string"
#
#   and then restart your terminal session. This will add the ``$IBMQE_API`` as an
#   environment variable that can be accessed by the script.
#   Once imported, you can check the values have set using print:
#   .. code-block:: python
#       import Qconfig
#       print(Qconfig.APItoken, Qconfig.config['url'])
# --------------------------------------------------------------------------------

import os

# Replace 'None' with your own API token (put it within quotes)
# Optionally, you can set the environment variable IBMQE_API as decribed in the
# aforementioned note. NOTE: If you set your APItoken below, it will OVERRIDE the
# value of the environment variable.

APItoken = None

config = {
  "url": 'https://quantumexperience.ng.bluemix.net/api'
}

def update_token(token=None):
    """Update the APItoken.

       :param token: The API token.(optional argument)
              If thisis set, it must be a string. The default value is None
    """
    global APItoken

    # If a token is given as an argument, use it.
    if token:
        APItoken = token
    else:
        # First check if APItoken is already set. If so, just use it.
        if APItoken:
            # Do nothing. The APItoken will override
            pass
        else:
            APItoken = os.getenv("IBMQE_API")

    assert (APItoken not in (None, '') and type(APItoken) is str), "Please set up a valid API access token. See Qconfig.py."

# Update the APItoken
update_token()

