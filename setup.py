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