"""Module for union class methods of ProxyVerse"""

from proxyverse.api.get_api import GetRequestProxyVerse
from proxyverse.api.post_api import PostRequestProxyVerse


class ApiProxyVerse:
    """Class for interacting with ProxyVerse API endpoints.

    This class provides a unified interface to the `GetRequestProxyVerse` and `PostRequestProxyVerse` methods.

    Attributes:
        post_request_verse (PostRequestProxyVerse): An instance of `PostRequestProxyVerse` for making POST requests.
        get_request_verse (GetRequestProxyVerse): An instance of `GetRequestProxyVerse` for making GET requests.

    Args:
        api_key (str): Your API key for accessing the ProxyVerse API.
    """


    def __init__(self, api_key: str) -> None:
        self.post_request_verse: PostRequestProxyVerse = PostRequestProxyVerse(api_key)
        self.get_request_verse: GetRequestProxyVerse = GetRequestProxyVerse(api_key)
