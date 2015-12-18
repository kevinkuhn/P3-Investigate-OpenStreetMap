#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import libraries
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
from codecs import open
import json
import string

# Import XML/OSM file into a directory
file_path = "source\lucerne.osm"
osm_file = open(file_path, "r")

# Find all the different tags within the dataset
# return them into a dictonary
def count_tags(filename):
    tag_count = {}
    for _, element in ET.iterparse(filename, events=("start",)):
        add_tag(element.tag, tag_count)
    return tag_count

def add_tag(tag, tag_count):
    if tag in tag_count:
        tag_count[tag] += 1
    else:
        tag_count[tag] = 1

"""
Function to check if we have problematic
characters within the street name. This will
be made to avoid that problematic characters
would be loaded into MongoDB
"""
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if lower.match(key):
            keys["lower"] = keys["lower"] + 1
        elif lower_colon.match(key):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif problemchars.match(key):
            keys["problemchars"] = keys["problemchars"] + 1
        else:
            keys["other"] = keys["other"] + 1

    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

# show all tags found in the dataset and count
pprint.pprint(count_tags(file_path))