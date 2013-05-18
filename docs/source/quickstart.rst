.. _quickstart:

Quickstart
==========

The beautiful thing about httpcache is that all you need is the quickstart
guide. Much like Requests has some very strong opinions about 'the right way'
to do HTTP, httpcache has some very strong opinions about 'the right way' to do
HTTP caching. This means there is essentially no configuration: httpcache is
built from the ground up to be plug-and-play.

Installing httpcache
--------------------

The recommended way to obtain a copy of httpcache is to get it from PyPI, using
``pip``. From your command-line shell, run::

    $ pip install httpcache

If you can't install httpcache using ``pip``, try using ``easy_install``::

    $ easy_install httpcache

Alternatively, download a
`gzipped tarball from PyPI <https://pypi.python.org/pypi/httpcache/0.1.0>`_.
If you extract that, you should find a ``setup.py`` file. You can install
httpcache by running::

    $ python setup.py install

Install The Adapter
-------------------

The expected way to use httpcache is to install the Requests Transport Adapter
that the module provides. This requires a couple of lines of code before you
start making web requests::

    import requests
    from httpcache import CachingHTTPAdapter

    s = requests.Session()
    s.mount('http://', CachingHTTPAdapter())
    s.mount('https://', CachingHTTPAdapter())

You can now use that Requests session just like normal. Under the covers,
httpcache takes care of all the caching decisions for you.

Using The Raw Cache
-------------------

Although it's not recommended, httpcache grudgingly allows you lower-level
access to the cache object itself. You can instantiate it like so::

    from httpcache import HTTPCache
    cache = HTTPCache()

You can then interact with the cache directly. Because it isn't recommended, no
further detail is given here.

**BE WARNED**: This API is considered 'semi-public'. The author reserves the
right to change this API as part of a minor version increase. If you are
interacting with the raw cache, be sure to consult the changelog before making
any minor version upgrade to determine whether the update will break your code.

Configuration
-------------

httpcache is firm in its belief that it knows what is best for you. This means
that there is very little in the way of configuration. In fact, you only have
one option: how many entries to cache. If you wanted to cache a maximum of 100
pages, then you would use::

    CachingHTTPAdapter(capacity=100)
