# -*- coding: utf-8 -*-
"""
cache.py
~~~~~~~~

Contains the primary cache structure used in http-cache.
"""
from .structures import RecentOrderedDict
from .utils import (parse_date_header, build_date_header,
                    expires_from_cache_control, url_contains_query)
from datetime import datetime


# RFC 2616 specifies that we can cache 200 OK, 203 Non Authoritative,
# 206 Partial Content, 300 Multiple Choices, 301 Moved Permanently and
# 410 Gone responses. We don't cache 206s at the moment because we
# don't handle Range and Content-Range headers.
CACHEABLE_RCS = (200, 203, 300, 301, 410)

# Cacheable verbs.
CACHEABLE_VERBS = ('GET', 'HEAD', 'OPTIONS')

# Some verbs MUST invalidate the resource in the cache, according to RFC 2616.
# If we send one of these, or any verb we don't recognise, invalidate the
# cache entry for that URL. As it happens, these are also the cacheable
# verbs. That works out well for us.
NON_INVALIDATING_VERBS = CACHEABLE_VERBS


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
        self._cache = RecentOrderedDict()

    def store(self, response):
        """
        Takes an HTTP response object and stores it in the cache according to
        RFC 2616.
        """
        # Define an internal utility function.
        def date_header_or_default(header_name, default, response):
            try:
                date_header = response.headers[header_name]
            except KeyError:
                value = default
            else:
                value = parse_date_header(date_header)
            return value

        if response.status_code not in CACHEABLE_RCS:
            return False

        if response.request.method not in CACHEABLE_VERBS:
            return False

        url = response.url
        now = datetime.utcnow()

        # Get the value of the 'Date' header, if it exists. If it doesn't, just
        # use now.
        creation = date_header_or_default('Date', now, response)

        # Get the value of the 'Cache-Control' header, if it exists.
        cc = response.headers.get('Cache-Control', None)
        if cc is not None:
            expiry = expires_from_cache_control(cc, now)

            # If the above returns None, we are explicitly instructed not to
            # cache this.
            if expiry is None:
                return False

        # Get the value of the 'Expires' header, if it exists, and if we don't
        # have anything from the 'Cache-Control' header.
        if cc is None:
            expiry = date_header_or_default('Expires', None, response)

        # If the expiry date is earlier or the same as the Date header, don't
        # cache the response at all.
        if expiry is not None and expiry <= creation:
            return False

        # If there's a query portion of the url and it's a GET, don't cache
        # this unless explicitly instructed to.
        if expiry is None and response.request.method == 'GET':
            if url_contains_query(url):
                return False

        self._cache[url] = {'response': response,
                            'creation': creation,
                            'expiry': expiry}

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
        return_response = None
        url = request.url

        try:
            cached_response = self._cache[url]
        except KeyError:
            return None

        if request.method not in NON_INVALIDATING_VERBS:
            del self._cache[url]
            return None

        if cached_response['expiry'] is None:
            # We have no explicit expiry time, so we weren't instructed to
            # cache. Add an 'If-Modified-Since' header.
            creation = cached_response['creation']
            header = build_date_header(creation)
            request.headers['If-Modified-Since'] = header
        else:
            # We have an explicit expiry time. If we're earlier than the expiry
            # time, return the response.
            now = datetime.utcnow()

            if now <= cached_response['expiry']:
                return_response = cached_response['response']
            else:
                del self._cache[url]

        return return_response
