# -*- coding: utf-8 -*-
"""
test-httpcache.py
~~~~~~~~~~~~~~~~~

Test cases for httpcache.
"""
import httpcache
from datetime import datetime


class TestHTTPCache(object):
    """
    Assorted tests of the HTTPCache object.
    """
    def test_can_store_responses(self):
        resp = MockRequestsResponse()
        cache = httpcache.HTTPCache()

        rc = cache.store(resp)
        assert rc

    def test_dont_store_non_200_responses(self):
        resp = MockRequestsResponse(status_code=403)
        cache = httpcache.HTTPCache()

        rc = cache.store(resp)
        assert not rc

    def test_can_retrieve_responses(self):
        resp = MockRequestsResponse()
        cache = httpcache.HTTPCache()

        cache.store(resp)
        cached_resp = cache.handle_304(resp)

        assert resp is cached_resp

    def test_can_extract_creation_date_from_response_RFC_1123(self):
        resp = MockRequestsResponse(headers={'Date': 'Sun, 06 Nov 1994 08:49:37 GMT'})
        cache = httpcache.HTTPCache()
        dt = datetime(1994, 11, 6, 8, 49, 37)

        cache.store(resp)

        assert cache._cache[resp.url]['creation'] == dt

    def test_can_extract_creation_date_from_response_RFC_850(self):
        resp = MockRequestsResponse(headers={'Date': 'Sunday, 06-Nov-94 08:49:37 GMT'})
        cache = httpcache.HTTPCache()
        dt = datetime(1994, 11, 6, 8, 49, 37)

        cache.store(resp)

        assert cache._cache[resp.url]['creation'] == dt

    def test_can_add_if_modified_since_header(self):
        resp = MockRequestsResponse(headers={'Date': 'Sun, 06 Nov 1994 08:49:37 GMT'})
        cache = httpcache.HTTPCache()
        req = MockRequestsPreparedRequest()

        cache.store(resp)
        cache.retrieve(req)

        assert req.headers['If-Modified-Since'] == 'Sun, 06 Nov 1994 08:49:37 GMT'

    def test_we_respect_the_expires_header(self):
        resp = MockRequestsResponse(headers={'Date': 'Sun, 06 Nov 1994 08:49:37 GMT',
                                             'Expires': 'Sun, 06 Nov 2034 08:49:37 GMT'})
        cache = httpcache.HTTPCache()
        req = MockRequestsPreparedRequest()

        cache.store(resp)
        cached_resp = cache.retrieve(req)

        assert cached_resp is resp


class MockRequestsResponse(object):
    """
    A specially-designed Mock object that emulates the behaviour of the
    post-v1.0.0 Requests Response object. For use with testing HTTPCache.
    """
    def __init__(self,
                 status_code=200,
                 headers={},
                 body='',
                 url='http://www.test.com/'):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.url = url


class MockRequestsPreparedRequest(object):
    """
    A specially-designed Mock object that emulates the behaviour of the
    post-v1.0.0 Requests PreparedRequest object. For use with testing
    HTTPCache.
    """
    def __init__(self,
                 method='GET',
                 headers={},
                 body='',
                 url='http://www.test.com/'):
        self.method = method
        self.headers = headers
        self.body = body
        self.url = url
