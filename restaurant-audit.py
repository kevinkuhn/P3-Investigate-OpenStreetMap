#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys

OSMFILE = "source\lucerne.osm"
restaurant_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# mapping definitions
mapping = { "Chimney?s" : "Chimeney's",
            "felsenegg": "Felsenegg",
            "KAFFEEPLUS": "KaffeePlus",
            "Mill?Feuille": "Mill'Feuille"
            }

# Create an audit for restaurant names
def audit_restaurant_types(restaurant_types, restaurant_name):
    m = restaurant_type_re.search(restaurant_name)
    # after restaurant_type_re has compiled an element
    if m:
        rest_type = m.group() 
        restaurant_types[rest_type].add(restaurant_name)
                   
# Returns the k attribute for XML list if it equal to a street address
def is_restaurant(elem):
    return (elem.attrib['k'] == "amenity")

def has_name(elem):
    return (elem.attrib['k'] == "name")

def update_name(name, mapping):
    st_type = restaurant_type_re.search(name).group()
    for x in mapping:
        if name.find(x)!=-1:
            new_name =  name.replace(x,mapping[x])
            print name,"=>",new_name
            name = new_name
    return name

# Create an audit an check with functions above
def audit(osmfile):
    osm_file = open(osmfile, "r")
    restaurant_types = defaultdict(set)
    # search for start events with iterparse, for example <tag...
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # search withing the python object for elements with the tag property == "way"
        if elem.tag == "node" or elem.tag == "amenity":
            # loop just within elements with <tag ... >
            setPass = False
            # Encoding of system
            stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()

            for tag in elem.iter("tag"):
                if setPass == True:
                    if tag.attrib['k'] == 'name':
                        # Clean up wrong restaurant names by using elements from the mapping
                        update_name(tag.attrib['v'].encode(stdout_encoding, errors='replace'),mapping)
                    setPass = False
                # if the k attribute of the tag is an amenity and v attribute is a restaurant then continue to audit
                # with setPass a "Gate" will be open to pass the attributes of the next element
                if tag.attrib['k'] == 'amenity' and tag.attrib['v'] == 'restaurant' :
                    setPass = True

                if is_restaurant(tag):
                    if has_name(tag):
                        # audit checks if it is an expected or unexpected street name based on attribute v
                        audit_restaurant_types(restaurant_types, tag.attrib['v'])
                        print restaurant_types
    return restaurant_types

def test():
    st_types = audit(OSMFILE)
    
    for st_type, ways in st_types.iteritems():
                    for name in ways:
                        better_name = update_name(name, mapping)
                        print name, "=>", better_name
                        
if __name__ == '__main__':
    test()