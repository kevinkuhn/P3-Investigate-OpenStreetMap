import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "source\lucerne.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Array with all the expected steet name endings
expected = ["strasse","Strasse", "platz",
			"weg","gasse","matt","matte",
			"halde", "quai", "ring", "hof",
			"weid"]

# mapping definitions
mapping = { "St" : "Street",
            "St.": "Street",
            "Rd." : "Road",
            "Ave": "Avenue"
            }

# Create an audit for street names that do not end with the expected street name endings
def audit_street_types(street_types, street_name):
    # check if a shorter form of street ending is used like "str." for "Strasse"
    check_ending(street_name, checkEnding)
    m = street_type_re.search(street_name)
    # if street_type_re has found an element
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

