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