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

from .utils import parse_date_header, build_date_header
from datetime import datetime


class HTTPCache(object):
    """
    The HTTP Cache object. Manages caching of responses according to RFC 2616,
    adding necessary headers to HTTP request objects, and returning cached
    responses based on server responses.
    """
    def __init__(self, capacity=50):
        #: The maximum capacity of the HTTP cache. When this many cache entries
        #: end up in the cache, the oldest entries are removed.
        self.capacity = capacity

        #: The cache backing store. Cache entries are stored here as key-value
        #: pairs. The key is the URL used to retrieve the cached response. The
        #: value is a python dict, which stores three objects: the response
        #: (keyed off of 'response'), the retrieval or creation date (keyed off
        #: of 'creation') and the cache expiry date (keyed off of 'expiry').
        #: This last value may be None.
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

        # Get the value of the 'Date' header, if it exists. If it doesn't, just
        # use now.
        try:
            date_header = response.headers['Date']
            creation = parse_date_header(date_header)
        except KeyError:
            creation = datetime.utcnow()

        # In the first implementation, we will just cache everything,
        # regardless of header value. Make sure that if we had an old cached
        # version we move the new one to the top of the cache.
        try:
            del self._cache[url]
        except KeyError:
            pass

        self._cache[url] = {'response': response,
                            'creation': creation,
                            'expiry': None}

        return True

    def handle_304(self, response):
        """
        Given a 304 response, retrieves the cached entry. This unconditionally
        returns the cached entry, so it can be used when the 'intelligent'
        behaviour of retrieve() is not desired.
        """
        try:
            cached_response = self._cache[response.url]['response']
        except KeyError:
            cached_response = None

        return cached_response

    def retrieve(self, request):
        """
        Retrieves a cached response if possible. If no cached response is
        immediately available, but it may be possible to re-use an old one,
        will attach an If-Modified-Since header to the request.
        """
        url = request.url

        cached_response = self._cache.get(url, None)

        if cached_response['expiry'] is None:
            # We have no explicit expiry time, so we weren't instructed to
            # cache. Add an 'If-Modified-Since' header.
            creation = cached_response['creation']
            header = build_date_header(creation)
            request.headers['If-Modified-Since'] = header

        return None
