# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~

Utility functions for use with httpcache.
"""
from datetime import datetime

RFC_1123_DT_STR = "%a, %d %b %Y %H:%M:%S GMT"
RFC_850_DT_STR = "%A, %d-%b-%y %H:%M:%S GMT"


def parse_date_header(header):
    """
    Given a date header in the form specified by RFC 2616, return a Python
    datetime object.

    RFC 2616 specifies three possible formats for date/time headers, and
    makes it clear that all dates/times should be in UTC/GMT. That is assumed
    by this library, which simply does everything in UTC. This currently does
    not parse the C asctime() string, because that's effort.

    This function does _not_ follow Postel's Law. If a format does not strictly
    match the defined strings, this function returns None. This is considered
    'safe' behaviour.
    """
    try:
        dt = datetime.strptime(header, RFC_1123_DT_STR)
    except ValueError:
        try:
            dt = datetime.strptime(header, RFC_850_DT_STR)
        except ValueError:
            dt = None

    return dt


def build_date_header(dt):
    """
    Given a Python datetime object, build a Date header value according to
    RFC 2616.

    RFC 2616 specifies that the RFC 1123 form is to be preferred, so that is
    what we use.
    """
    return dt.strftime(RFC_1123_DT_STR)
