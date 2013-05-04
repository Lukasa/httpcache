# -*- coding: utf-8 -*-
"""
cache.py
~~~~~~~~

Contains the primary cache structure used in http-cache.
"""


class HTTPCache(object):
    """
    The HTTP Cache object. Manages caching of responses according to RFC 2616,
    adding necessary headers to HTTP request objects, and returning cached
    responses based on server responses.
    """
    def __init__(self, capacity=50):
        self.capacity = capacity

    def store(self, response):
        """
        Takes an HTTP response object and stores it in the cache according to
        RFC 2616.
        """
        pass

    def retrieve(self, request):
        """
        Retrieves a cached response if possible. If no cached response is
        immediately available, but it may be possible to re-use an old one,
        will attach an If-Modified-Since header to the request.
        """
        pass
