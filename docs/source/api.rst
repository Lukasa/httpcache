.. _api:

Interfaces
==========

.. module:: httpcache

This section of the documentation discusses the httpcache interface.


Caching HTTP Adapter
--------------------

The Caching HTTP Adapter is the recommended interface to httpcache. A transport
adapter that plugs directly into a Requests session, this represents the
easiest way to add caching to Requests.

.. autoclass:: httpcache.CachingHTTPAdapter
   :inherited-members:

HTTP Cache
----------

The HTTP Cache is the object that backs the Caching HTTP Adapter. This provides
the primary caching functionality. The object is documented here for reference
and for developers who believe they need better control over the caching
behaviour than the Caching HTTP Adapter provides.

**BE WARNED**: This API is considered 'semi-public'. The author reserves the
right to change this API in a minor version increase, rather than having to
wait for a major version increase as per
`Semantic Versioning <http://semver.org/>`_.

.. autoclass:: httpcache.HTTPCache
   :inherited-members:
