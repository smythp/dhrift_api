import requests
from urllib.error import HTTPError
from keys import CLIENT_ID, CLIENT_SECRET

BASEURL = "https://api.github.com"

AUTHORIZE_BASEURL = 'https://github.com/login/oauth/authorize'
ACCESS_TOKEN_BASEURL = 'https://github.com/login/oauth/access_token'




def build_url(baseurl, query_parameters):
    """Build a URL from a baseurl and a dictionary of query parameters."""
    parameter_strings = []

    for key in query_parameters:
        
        
        parameter_strings.append('='.join([
            str(key),
            str(query_parameters[key])
            ]
        ),)

    parameters = '&'.join(
        parameter_strings
    )

    return '?'.join([
        baseurl, parameters
    ])
    
def code_request_url(login=None):
    """Create a URL for users to authenticate. The code is returned as a query parameter."""

    parameters = {
        'client_id' : CLIENT_ID
        }

    if login:
        parameters['login'] = login


    return build_url(AUTHORIZE_BASEURL, parameters)


def get_bearer_token(code):
    """Using the code given during authentication, get a bearer token used to authenticate to the API."""

    parameters = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
        }

    url = build_url(ACCESS_TOKEN_BASEURL, parameters)

    r = requests.get(url)

    if not r.ok:
        raise HTTPError('Not a 200 response')

    return_parameters = r.text.split('&')
    token = return_parameters[0].split('=')[1]
    

    return token
