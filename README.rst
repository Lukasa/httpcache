http-cache: HTTP Caching for Python
===================================

HTTP, like all well designed standards, has multiple confusing mechanisms for
caching. This module is a HTTP cache that knows how to use HTTP headers and
status codes to correctly cache your HTTP traffic. It's built for use with the
excellent `Requests <https://github.com/kennethreitz/requests>`_ library,
because if you're not using Requests you're probably prepared to roll your own
caching library too.

It's gloriously easy to use. Store your cache entries like this:

.. code-block:: python

    from httpcache import HTTPCache
    cache = HTTPCache(capacity=50)
    cache.store(response)

And retrieve them like this:

.. code-block:: python

    cached_response = cache.retrieve(request)

Simple.

Features
--------

- Tight integration with `Requests <https://github.com/kennethreitz/requests>`_
  data structures.
- Understands ``Expires`` and ``Cache-Control`` headers.
- Knows how to interpret ``304 Not Modified`` responses.
- Can send ``If-Modified-Since`` headers.
- Aware of HTTP verbs, e.g. ``POST``.
- RFC 2616-compliant.

Installation
------------

To install http-cache, you want to run:

.. code-block:: bash

    $ pip install http-cache

If you can't do that, and you really must have http-cache, and you can't
install ``pip``, then you can try:

.. code-block:: bash

    $ easy_install http-cache

I strongly recommend you don't do that though.

Contribute
----------

Contributions are always welcome! Please abide by the following rules when
contributing:

#. Check that no-one has opened an issue already covering your bug. If you open
   a duplicate issue, the maintainer will give you a stern look.
#. Fork the `Github repository`_ and start writing your tests. If you're fixing
   a bug, I recommend writing a failing test first and working until it passes.
   If you're adding a feature, you're free to add tests after you write the
   functionality, but please test the functionality thoroughly.
#. Send a Pull Request. If I don't respond within a couple of days, please
   shout at me on Twitter or via email until I do something about it.

.. _`Github repository`: https://lukasa.co.uk/
