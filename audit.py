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