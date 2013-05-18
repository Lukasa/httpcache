History
-------

0.1.1 (2013-05-18)
++++++++++++++++++

* Cache a broader set of response codes.
* Follow RFC 2616's recommendations about caching resources with query strings.
* Don't cache non-idempotent methods.
* Non-idempotent methods invalidate their cache resources.
* Documentation!
* Actually implement the capacity parameter.

0.1.0 (2013-05-11)
++++++++++++++++++

* Provide a Requests Transport Adapter so that caching 'Just Works'.

0.0.2 (2013-05-07)
++++++++++++++++++

* Correctly cache using the 'Expires' header.
* Correctly handle some of the functionality exposed by the 'Cache-Control' header.

0.0.1 (2013-05-05)
++++++++++++++++++

* Conception
* If-Modified-Since and 304 handling.
