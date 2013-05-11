"""
adapter.py
~~~~~~~~~~

Contains an implementation of an HTTP adapter for Requests that is aware of the
cache contained in this module.
"""
from requests.adapters import HTTPAdapter
from .cache import HTTPCache

class CachingHTTPAdapter(HTTPAdapter):
    """
    A HTTP-caching-aware Transport Adapter for Python Requests.
    """
    def __init__(self, capacity=50, **kwargs):
        super(CachingHTTPAdapter, self).__init__(**kwargs)

        self.cache = HTTPCache(capacity=capacity)

    def send(self, request, **kwargs):
        """
        Sends a PreparedRequest object, respecting RFC 2616's rules about HTTP
        caching. Returns a Response object that may have been cached.
        """
        pass

    def build_response(self, request, response):
        """
        Builds a Response object from a urllib3 response. May involve returning
        a cached Response.
        """
        pass
