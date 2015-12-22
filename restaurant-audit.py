#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys

OSMFILE = "source\lucerne.osm"
restaurant_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Array with all the expected steet name endings
expected = []

# mapping definitions
mapping = { "Chimney?s" : "Chimeney's",
            "felsenegg": "Felsenegg",
            "KAFFEEPLUS": "KaffeePlus",
            "Mill?Feuille": "Mill'Feuille"
            }

# Create an audit for street names that do not end with the expected street name endings

def audit_restaurant_types(restaurant_types, street_name):
    m = restaurant_type_re.search(street_name)
    # if street_type_re has found an element
    if m:
        rest_type = m.group() 
        # loop to check if the steet name ending matches with one of the endings for the expected list
        #for check not in expected:
        restaurant_types[rest_type].add(street_name)
                   

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
    # search for start events with iterparse, for exampla <way...
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
                        # Print restaurant name with replacing missing/wrong chracters
                        #print tag.attrib['v'].encode(stdout_encoding, errors='replace')
                        update_name(tag.attrib['v'].encode(stdout_encoding, errors='replace'),mapping)
                    setPass = False
                # if the k attribute of the tag is a street address then continue to audit
                if tag.attrib['k'] == 'amenity' and tag.attrib['v'] == 'restaurant' :
                    setPass = True

                if is_restaurant(tag):
                    if has_name(tag):
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
    
    for st_type, ways in st_types.iteritems():
                    for name in ways:
                        better_name = update_name(name, mapping)
                        print name, "=>", better_name
                        if name == "paradiesgässli":
                            assert better_name == "Paradiesgässli"
    


if __name__ == '__main__':
    test()



'''
  <node id="259538738" lat="47.0302022" lon="8.2922993" version="3" timestamp="2010-12-07T06:46:38Z" changeset="6571374" uid="74900" user="FischersFritz"/>
  <node id="259538740" lat="47.0310623" lon="8.2929684" version="5" timestamp="2010-12-07T06:46:32Z" changeset="6571374" uid="74900" user="FischersFritz"/>
  <node id="259538742" lat="47.0296533" lon="8.2938757" version="3" timestamp="2010-12-07T06:46:24Z" changeset="6571374" uid="74900" user="FischersFritz"/>
  <node id="259538743" lat="47.0296138" lon="8.2937561" version="2" timestamp="2010-12-07T06:46:37Z" changeset="6571374" uid="74900" user="FischersFritz">
    <tag k="amenity" v="restaurant"/>
    <tag k="name" v="Giovannini's"/>
  </node>
  <node id="259538745" lat="47.0287082" lon="8.2977724" version="3" timestamp="2011-01-04T20:04:55Z" changeset="6864989" uid="74900" user="FischersFritz"/>
  <node id="259538746" lat="47.0291184" lon="8.2974528" version="3" timestamp="2011-01-04T20:05:24Z" changeset="6864989" uid="74900" user="FischersFritz"/>
  '''