#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

setup = [ "version", "changeset", "timestamp", "user", "uid"]

def is_address(elem):
    if elem.attrib['k'][:5] == "addr:":
        return True

def shape_element(element):
    node = {}
    
    if element.tag != "node" and element.tag != "way" :
        return None
    else:
        node['type']    = element.tag        
        node['pos']     = [None,None]

        for key in element.keys():
            if key in setup:
                node.setdefault('created', {})
                node['created'][key] = element.get(key)
            elif key == "lat":
                node['pos'][0] = float(element.get(key))
            elif key == "lon":
                node['pos'][1] = float(element.get(key))
            else:
                node[key] = element.get(key)

        for child_element in iter(element):
            if child_element.tag == "nd":
                node.setdefault('node_refs', []).append(child_element.attrib["ref"])
            elif child_element.tag == "tag":
                key = child_element.attrib["k"]
                if (problemchars.search(key)):
                    continue
                elif(key.startswith('addr:')):
                    node.setdefault('address', {})
                    addr = key.split(':')
                    
                    if(len(addr)==2):
                        key = addr[1]
                        node['address'][key] = child_element.attrib["v"]
                else:
                    node[key] = child_element.attrib["v"]
        return node


def process_map(file_in, pretty):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('source/lucerne.osm', True)
    #pprint.pprint(data)
    print data[0]
    
    correct_first_elem = {
    'id': '780188', 
    'type': 'node', 
    'pos': [47.0537166, 8.2545779], 
    'created': {
        'changeset': '6577828', 
        'user': 'aMuTeX', 
        'version': '5', 
        'uid': '75217', 
        'timestamp': '2010-12-07T18:29:07Z'
        }
    }
    assert data[0] == correct_first_elem

if __name__ == "__main__":
    test()