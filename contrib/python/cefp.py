#!/usr/bin/env python

"""
LICENSE - see LICENSE file in the root of this repository

The parse_cef function accepts a string of cef key value pairs and returns a
dictionary of those pairs.

POSSIBLE FUTURE ENHANCEMENTS
-------------------
- Detect date formatted strings and automatically attempt to convert to a
  datetime object
"""

import re

cef_re_pairs = re.compile("(\w+)=(.*)")
cef_re_split = re.compile(" (?=\w+=)")

def parse_cef(s):
    """ returns dict of k/v extracted from cef string """
    d = dict()
    for c in [cef_re_pairs.findall(kv) for kv in cef_re_split.split(s) if kv]:
        for cc in c:
            if isinstance(cc, tuple) and len(cc)==2: d[cc[0]] = cc[1]
    return d
