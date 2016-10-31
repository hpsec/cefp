#!/usr/bin/env python
from __future__ import print_function

"""
LICENSE - see LICENSE file in the root of this repository

The parse_cef function accepts a string of cef key value pairs and returns a
dictionary of those pairs.

POSSIBLE FUTURE ENHANCEMENTS
-------------------
- Detect date formatted strings and automatically attempt to convert to a
  datetime object
"""

import json
import re
import fileinput


cef_key_re = re.compile(r" ([\w.-]+?)=")
cef_first_key_re = re.compile(r"([\w.-]+?)=")
cef_pipe_re = re.compile(r"\\*?\|")

def parse_cef(s):
    d = dict()
    fields = []
    field_start = 0
    for match in cef_pipe_re.finditer(s):
        start, end = match.span()
        if (end-start)%2==0:
            # There are an odd number of backslashes, so the pipe is escaped.
            # A negative lookbehind may be a better way to do this.
            continue
        field = s[field_start:end-1]
        fields.append(field.replace("\\|","|").replace("\\\\","\\"))
        field_start = end
        if len(fields)==7:
            break
    else:
        raise ValueError("CEF string does not have enough pipe characters")

    if 'CEF:0' not in fields[0]:
        raise ValueError("CEF string is missing CEF:0 header")

    d["devicevendor"] = fields[1]
    d["deviceproduct"] = fields[2]
    d["deviceversion"] = fields[3]
    d["signatureid"] = fields[4]
    d["name"] = fields[5]
    d["severity"] = fields[6]

    parse_cef_extension(d, s[field_start:])
    if '_cefVer' not in d:
        raise ValueError("CEF string is missing _cefVer")
    return d

def parse_cef_extension(d, s):
    last_start = len(s)
    matches = cef_key_re.finditer(s)
    # Look at the key value pairs from the end to the beginning because the
    # only way to find the end of a value is to find the start of the next key.
    for match in reversed(list(matches)):
        start, end = match.span()
        d[match.group(1)] = unescape_cef_value(s[end:last_start])
        last_start = start

    # The first key-value pair may be preceded by a space. If it is not, add
    # it to d .
    leftover = s[:last_start]
    match = cef_first_key_re.match(leftover)
    if match:
        d[match.group(1)] = unescape_cef_value(s[match.end():last_start])
    return d

def unescape_cef_value(s):
    s = s.replace("\\r","\r").replace("\\n", "\n")
    return s.replace("\\=","=").replace("\\\\", "\\")

def cef2json(line):
    return json.dumps(parse_cef(line))

def item_as_cef(item):
    HEADER_KEYS = ["devicevendor", "deviceproduct", "deviceversion",
                   "signatureid", "name", "severity"]
    header = ["" for _ in HEADER_KEYS]
    extension = {}
    for key,value in item.iteritems():
        if key in HEADER_KEYS:
            esc = value.replace('\\','\\\\').replace('|','\\|')
            header[HEADER_KEYS.index(key)] = esc.encode('utf-8')
        elif key=='_cefVer':
            continue
        else:
            if isinstance(value,basestring):
                value = value.replace('\\','\\\\').replace('=','\\=')
                value = value.replace('\r','\\r').replace('\n','\\n')
                extension[key] = value.encode('utf-8')
            else:
                extension[key] = str(value)

    header_str = "|".join(header)
    extension_str = " ".join(
        "{}={}".format(key,value)
        for key,value in extension.iteritems()
    )
    return "CEF:0|{}|{} _cefVer=0.1\n".format(header_str,extension_str)

def json2cef(line):
    return item_as_cef(json.loads(line))

if __name__ == '__main__':
    for line in fileinput.input():
        print(cef2json(line.rstrip('\n')))


