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

'''def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        for key in element.attrib.keys():
            val = element.attrib[key]
            node["type"] = element.tag
            if key in setup:
                if not "created" in node.keys():
                    node["created"] = {}
                node["created"][key] = val
            elif key == "lat" or key == "lon":
                if not "pos" in node.keys():
                    node["pos"] = [0.0, 0.0]
                old_pos = node["pos"]
                if key == "lat":
                    new_pos = [float(val), old_pos[1]]
                else:
                    new_pos = [old_pos[0], float(val)]
                node["pos"] = new_pos
            else:
                node[key] = val
            for tag in element.iter("tag"):
                tag_key = tag.attrib['k']
                tag_val = tag.attrib['v']
                if tag_key == "addr:street":
                    # check if steet name fits to conventions (function update_name)
                    tag_val = update_name(tag_val)
                if problemchars.match(tag_key):
                    continue
                elif tag_key.startswith("addr:"):
                    if not "address" in node.keys():
                        node["address"] = {}
                    addr_key = tag.attrib['k'][len("addr:") : ]
                    if lower_colon.match(addr_key):
                        continue
                    else:
                        node["address"][addr_key] = tag_val
                elif lower_colon.match(tag_key):
                    node[tag_key] = tag_val
                else:
                    node[tag_key] = tag_val
        for tag in element.iter("nd"):
            if not "node_refs" in node.keys():
                node["node_refs"] = []
            node_refs = node["node_refs"]
            node_refs.append(tag.attrib["ref"])
            node["node_refs"] = node_refs

        return node
    else:
        return None'''

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
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
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
    '''
                assert data[-1]["address"] == {
                                                "street": "West Lexington St.", 
                                                "housenumber": "1412"
                                                  }
                assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                                "2199822370", "2199822284", "2199822281"]'''

if __name__ == "__main__":
    test()