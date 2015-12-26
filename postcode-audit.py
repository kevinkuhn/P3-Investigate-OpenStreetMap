#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import csv
import os

########### LOAD CSV FILE WITH POSTCODES ###########

DATADIRCSV = "source/"
DATAFILECSV = "mapping-post-codes.csv"

postcodes = []

def parse_csv(datafile):
    
    postcodeNamesCSV = []
    
    n = 0
    with open(datafile,'rb') as sd:
        r = csv.DictReader(sd)
        for line in r:
            postcodeNamesCSV.append({'postcode' : line["postcode"], 'name' : line["streetName"]})
            if line["postcode"] not in postcodes:
                # add the postocode if it is not already in the array > to get the unique postcodes for Lucerne
                postcodes.append(line["postcode"])
    return postcodeNamesCSV

########### LOAD OSM FILE FROM OPENSTREETMAP ###########

OSMFILE = u"source\lucerne.osm"
postcode_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Create an audit for postcode that do not end with the expected postcodes
def audit_postcode_types(postcode_types, postcode):
    m = postcode_type_re.search(postcode)
    # after postcode_type_re has compiled an element
    if m:
        postcode_type = m.group() 
        if postcode_type not in expected:
            postcode_types[postcode_type].add(postcode)
    
    return postcode_types

# Returns the k attribute for XML list if it equal to a postcode
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def has_name(elem):
    return (elem.attrib['k'] == "addr:name")

def update_name(name, mapping):
    st_type = postcode_type_re.search(name).group()
    for x in mapping:
        if name.find(x)!=-1:
            name =  name.replace(x,mapping[x])
    return name

# Create an audit an check with functions above
def audit(osmfile):
    osm_file = open(osmfile, "r")
    postcode_types = defaultdict(set)

    pcode = ""
    pcodeName = ""
    postcodeNames = []

    # search for start events with iterparse, for example <way...
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # search withing the python object for elements with the tag property == "way"
        if elem.tag == "node" or elem.tag == "way":
            # loop just within elements with <tag ... >
            for tag in elem.iter("tag"):
                # if the k attribute of the tag is a postcode then continue to audit
                if tag.attrib["k"] == "addr:postcode":
                    pcode = tag.attrib["v"]
                if tag.attrib["k"] == "name":
                    pcodeName = tag.attrib["v"] #.decode('utf-8').encode(stdout_encoding, errors='ignore')
            if pcode != "" and pcodeName != "":
                postcodeNames.append({'postcode' : pcode, 'name' : pcodeName}) #.encode(stdout_encoding, errors='ignore')})
                #reset
                pcode, pcodeName = "",""
            # start audit
            #audit_postcode_types(postcode_types, tag.attrib['v'])
    return postcodeNames

def compare_csv(osmOutput,csvOutput):
    print "Number of entries in OSM file",len(osmOutput)
    print "Number of entries in CSV file",len(csvOutput)
    for element in osmOutput:
        if element['name'] != "":
            for checks in csvOutput:
                if element['name'] == checks['name']:
                    if element['postcode'] != checks['postcode']:
                        print "Different postcodes: ",element['name'],element['postcode'],"=>",checks['name'],checks['postcode']
                        # Change postcodes
                        element['postcode'] =  element['postcode'].replace(element['postcode'],checks['postcode'])

if __name__ == '__main__':
    pc_types_osm = audit(OSMFILE)
    datafile_csv = os.path.join(DATADIRCSV, DATAFILECSV)
    pc_types_csv = parse_csv(datafile_csv)
    compare_csv(pc_types_osm,pc_types_csv)