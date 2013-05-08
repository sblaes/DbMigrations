#!/usr/bin/env python

import re
import httplib
from datetime import datetime, tzinfo, timedelta
from sys import exit

# Borrowed shamelessly from python documentation at
# http://docs.python.org/library/datetime.html#datetime.tzinfo

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

# A UTC class.

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

URIS = []

def getRequestToUri(server, uri):
    conn = httplib.HTTPConnection(server)
    conn.request("GET", uri)
    resp = conn.getresponse()
    return resp.read()

def ident(word):
    return word

def yahooFormat(result):
    result = result.replace("\"", "'").strip()
    s = re.sub(r"{'Result':{'Timestamp':(\d+)}}", r"\1", result).strip()
    return s

# Yahoo Time uri
URIS.append(["developer.yahooapis.com", "/TimeService/V1/getTime?appid=foo&output=json", yahooFormat])

def getDatestampFromTimestamp(timestamp):
    f = 0.0;
    if(isinstance(timestamp, float)):
        f = timestamp
    else:
        f = float(timestamp)
    d = datetime.fromtimestamp(f, utc)
    return d.strftime("%Y%m%d%H%M%S")

def success(msg=None):
    if(msg != None):
        print(msg)
    exit(0)

def fail(msg=None):
    if(msg != None):
        print(msg)
    exit(1)

def getTime():
    for uri in URIS:
        return getDatestampFromTimestamp(uri[2](getRequestToUri(uri[0], uri[1])))

if(__name__ == "__main__"):
    print(getTime())
