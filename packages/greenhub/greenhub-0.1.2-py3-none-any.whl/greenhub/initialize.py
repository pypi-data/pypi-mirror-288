import requests
from typing import Optional
from urllib.error import HTTPError

from .utilities.feature_data_cache import FeatureDataCache


API_KEY_CHECK_REST_API_URL: str = 'https://us-central1-digitalyieldmonitoringplatform.cloudfunctions.net/checkApiKey'

user_api_key: Optional[str] = None
fdc: Optional[FeatureDataCache] = None


def initialize(api_key: str):
    """
    Initialize the greenhub SDK.
    It is important to initialize the greenhub SDK before using any further functionalities of the SDK.
    The given `api_key` is verified, and an error is thrown only if the API key is not valid.

    :param api_key: user API key derived from greenhub.ai
    :throws ValueError: if the API key is not valid
    """

    global user_api_key
    global fdc

    # check if api key is valid
    res = requests.get(API_KEY_CHECK_REST_API_URL, params={'apiKey': api_key})
    if res.status_code == 200:
        user_api_key = api_key
        fdc = FeatureDataCache()
    elif res.status_code == 401:
        raise ValueError("Invalid API key.")
    else:
        raise HTTPError(f'Checking API key failed with status code: {res.status_code}')


def get_user_api_key() -> Optional[str]:
    global user_api_key
    return user_api_key


def get_fdc() -> Optional[FeatureDataCache]:
    global fdc
    return fdc


