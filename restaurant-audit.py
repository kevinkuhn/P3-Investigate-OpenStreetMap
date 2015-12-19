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
expected = ["strasse", "platz", "weg",
			"allee","gasse","matt","matte",
			"halde", "quai", "ring", "hof",
			"weid", "höhe", "wil", "egg"]

# mapping definitions
mapping = { "str." : "strasse",
            "Alee": "Allee",
            "Alle": "Allee",
            u"gäsli" : u"gässli",
            u"paradiesgässli" : u"Paradiesgässli"
            }

# Create an audit for street names that do not end with the expected street name endings

def audit_restaurant_types(restaurant_types, street_name):
    m = street_type_re.search(street_name)
    # if street_type_re has found an element
    if m:
        street_type = m.group() 
        myLoops = 0
        # loop to check if the steet name ending matches with one of the endings for the expected list
        for check in expected:
            if check not in expected:
                restaurant_types[street_type].add(street_name)
                   

# Returns the k attribute for XML list if it equal to a street address
def is_restaurant(elem):
    return (elem.attrib['k'] == "restauant")
'''
def set_utf8(message):
    import sys
    # Change message into unicode and compile it with the defined charset
    return message.decode("utf-8").encode(sys.stdout.encoding)
'''

'''
def update_name(name, mapping):
    st_type = street_type_re.search(name).group()
    for x in mapping:
        if name.find(x)!=-1:
            name =  name.replace(x,mapping[x])
    return name
'''
# Create an audit an check with functions above
def audit(osmfile):
    osm_file = open(osmfile, "r")
    restaurant_types = defaultdict(set)
    # search for start events with iterparse, for exampla <way...
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # search withing the python object for elements with the tag property == "way"
        if elem.tag == "node" or elem.tag == "amenity":
            # loop just within elements with <tag ... >
            for tag in elem.iter("tag"):
                # if the k attribute of the tag is a street address then continue to audit
                if is_restaurant(tag):
                    # audit checks if it is an expected or unexpected street name based on attribute v
                    audit_restaurant_types(restaurant_types, tag.attrib['v'])
                    print restaurant_types
    # print out the list of unexpected street names as a dictonary
    #pprint.pprint(dict(restaurant_types))
    # print the number of streets that do not fit to the expectations
    #print len (restaurant_types)
    return restaurant_types

def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))
    '''
    for st_type, ways in st_types.iteritems():
                    for name in ways:
                        better_name = update_name(name, mapping)
                        print name, "=>", better_name
                        if name == "paradiesgässli":
                            assert better_name == "Paradiesgässli"
    '''


if __name__ == '__main__':
    test()