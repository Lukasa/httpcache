# -*- coding: utf-8 -*-
"""
cache.py
~~~~~~~~

Contains the primary cache structure used in http-cache.
"""
try:
    from collections import OrderedDict
except ImportError:
    # We need to do something for earlier Python compatibility. Handle this
    # later.
    pass


class HTTPCache(object):
    """
    The HTTP Cache object. Manages caching of responses according to RFC 2616,
    adding necessary headers to HTTP request objects, and returning cached
    responses based on server responses.
    """
    def __init__(self, capacity=50):
        self.capacity = capacity
        self._cache = OrderedDict()

    def store(self, response):
        """
        Takes an HTTP response object and stores it in the cache according to
        RFC 2616.
        """
        # To begin with we only cache 200 OK responses.
        if response.status_code != 200:
            return False

        url = response.url

        # In the first implementation, we will just cache everything,
        # regardless of header value. Make sure that if we had an old cached
        # version we move the new one to the top of the cache.
        try:
            del self._c[url]
        except KeyError:
            pass

        self._c[url] = response

        return True

    def retrieve(self, request):
        """
        Retrieves a cached response if possible. If no cached response is
        immediately available, but it may be possible to re-use an old one,
        will attach an If-Modified-Since header to the request.
        """
        pass
