#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys

OSMFILE = "source\lucerne.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Array with all the expected steet name endings
expected = ["-Strasse", "strasse", "platz", "weg",
			"allee","gasse","matt","matte",
			"halde", "quai", "ring", "hof",
			"weid", "höhe", "wil", "egg"]

# mapping definitions
mapping = { u"str." : u"strasse",
            u"Alee": u"Allee",
            u"Alle": u"Allee",
            u"gäsli" : u"gässli",
            u"dorv" : u"dorf",
            u"gase" : u"gasse",
            u"veg" : u"weg",
            u"höffli" : u"höfli",
            u"rein" : u"rain",
            u"paradiesgässli" : u"Paradiesgässli"
            }
# Create an audit for street names that do not end with the expected street name endings
def audit_street_types(street_types, street_name):
    m = street_type_re.search(street_name)
    # after street_type_re has compiled an element
    if m:
        street_type = m.group() 
        myLoops = 0
        # loop to check if the steet name ending matches with one of the endings for the expected list
        for check in expected:
            # cut of the ending of the street name and compare it with one of the expected words
            if street_type[len(street_type)-len(check):len(street_type)] != check:
                myLoops += 1
                # if loop limit reached (no match with the expected endings) the street name will be added to a list
                if myLoops == len(expected):
                    street_types[street_type].add(street_name)
                    myLoops = 0 # reset of the loop when loop limit reached

# Returns the k attribute for XML list if it equal to a street address
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def set_utf8(message):
	import sys
	# Change message into unicode and compile it with the defined charset
	return message.decode("utf-8").encode(sys.stdout.encoding)

def update_name(name, mapping):
    st_type = street_type_re.search(name).group()
    for x in mapping:
        if name.find(x)!=-1:
            name =  name.replace(x,mapping[x])
    return name

# Create an audit an check with functions above
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    # search for start events with iterparse, for example <way...
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # search withing the python object for elements with the tag property == "way"
        if elem.tag == "node" or elem.tag == "way":
            # loop just within elements with <tag ... >
            for tag in elem.iter("tag"):
                # if the k attribute of the tag is a street address then continue to audit
                if is_street_name(tag):
                    # audit checks if it is an expected or unexpected street name based on attribute v
                    audit_street_types(street_types, tag.attrib['v'])
    # print out the list of unexpected street names as a dictonary
    #pprint.pprint(dict(street_types))
    # print the number of streets that do not fit to the expectations
    #print len (street_types)
    return street_types

def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "paradiesgässli":
                assert better_name == "Paradiesgässli"


if __name__ == '__main__':
    test()