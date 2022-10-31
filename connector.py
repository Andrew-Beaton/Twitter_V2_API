from time import sleep
from datetime import datetime
import requests
import private 
import logging

def bearer_auth(r:object):
    """_summary_

    Args:
        r (object): Required object by authentication with bearer token

    Returns:
        _type_: filled out object for authentication with bearer token
    """    
    r.headers["Authorization"] = f"Bearer {private.get_bearer_token()}"
    r.headers["User-Agent"] = "LumilinksTwitter"
    return r 


def endpoint_connector (url:str, params:dict):
    """_summary_

    Args:
        url (str): This  is the twitter end point url 
        params (dict): Contains the details of the query to the api, this changes for each query and endpoint

    Raises:
        Exception: If non 200 http status code is recieved an exception is raised

    Returns:
        json: Api returns results as a json this is returned by the function
    """    
    #logging.debug(f"parameters at the connector are {params}")
    response = requests.request("GET", url, auth=bearer_auth, params=params)
    

    if response.status_code != 200:
        logging.warning(response.status_code)
        logging.warning(response.text)
    if response.status_code == 429:
        logging.warning(f"A request was rate limited, now waiting 15 minutes for rate reset.Starting at {datetime.now()}")
        sleep(900)
        response = requests.request("GET", url, auth=bearer_auth, params=params)

    return response.json()

def url_only_connector(url:str):

    #logging.debug("Started url connector")
    response = requests.request("GET",url,auth = bearer_auth)


    if response.status_code !=200:
        logging.error(f"There was an error in the url only process using url = {url}")
        logging.error(response.text)
    if response.status_code == 429:
        logging.warning(f"A request was rate limited, now waiting 15 minutes for rate reset. Starting at {datetime.now()}")
        sleep(900)
        response = requests.request("GET",url,auth = bearer_auth)
    #logging.debug("Finished Url only connection")
    return response.json()