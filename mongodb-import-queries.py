#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import subprocess

filename="lucerne.osm"

########################## CONNECT MONGODB ##########################

from pymongo import MongoClient
db_name = "osm"

client = MongoClient('localhost:27017')
db = client[db_name]

########################## IMPORT JSON ##########################

# Build mongoimport command
collection = filename[:filename.find(".")]
working_directory = "source/"
json_file = filename + ".json"

# Before importing, drop collection if it exists
if collection in db.collection_names():
    print "dropping collection"
    db[collection].drop()

# execute import command by cmd
mongoimport_cmd = "mongoimport --db " + db_name + \
                  " --collection " + collection + \
                  " --file " + working_directory + json_file

# Execute import command by cmd
print "Executing: " + mongoimport_cmd
subprocess.call(mongoimport_cmd.split())

########################## QUERIES ##########################

entries = db.lucerne

# Number of documents
print "Number of documents:", entries.find().count()
                                                
# Number of nodes
print "Number of nodes:", entries.find({"type":"node"}).count()

# Number of ways
print "Number of ways", entries.find({"type":"way"}).count()

def find():
    
    projection = {"_id" : 0, "address.street" : 1}
        
    streets = entries.find({"address.street" : {"$exists": 1}}, projection)
    
    print "number of entries without street name: ",entries.find({"address.street" : {"$exists": 0}}, projection).count()
    print "number of entries with street name: ",entries.find({"address.street" : {"$exists": 1}}, projection).count()
    print "number of entries with street name that contains 'Strasse': ",entries.find({"address.street" : {"$exists": 1},"address.street" : {"$regex": "[Ss]trasse"}}, projection).count()
    
    expected = ["strasse","Strasse", "platz", "weg","gasse","str.","matt","matte","halde", "quai", "ring", "hof", "weid"]
    vLabels = []
    vCounts = []

    for e in expected:
        vLabels.append(e)
        numOfCount = entries.find({"address.street" : {"$exists": 1},"address.street" : {"$regex": e}}, projection).count()
        vCounts.append(numOfCount)
        print "number of entries with street name that contains ", e,": ", numOfCount

    from visualize import pie_chart
    pie_chart(vLabels,vCounts,"Street-Name-Endings")

find()

def find_restaurant_by_postcode(postcode,typeOfRestaurant):
    projection = {"_id" : 0, "amenity" : 1, "cuisine" : 1, "name" : 1, "address.street" : 1, "address.postcode" : 1}
    return entries.find({ "$and": [ {"address.postcode" : {"$eq" : str(postcode)}},
                                {"amenity": {"$eq" : "restaurant"}},
                                {"cuisine": {"$eq" : str(typeOfRestaurant)}},
                                {"name": {"$exists": 1}},
                                {"address.street": {"$exists": 1}} ] }, projection)

#find a vegetarian restaurant in my hometown
typeOfRestaurant = "vegetarian"
postcode = 6006
print "Searching for an",typeOfRestaurant,"restaurant in the area of postcode",postcode,"..."
pprint.pprint(list(find_restaurant_by_postcode(postcode, typeOfRestaurant)))


# Print out the 5 most active user
def most_active_useres():
    pipeline = [{"$group": { "_id": "$created.user", "count": { "$sum" : 1} } },
    { "$sort": { "count": -1 } },
    {"$limit" : 5}]
    return list(entries.aggregate(pipeline))

pprint.pprint(most_active_useres())

def wheelchair_friendly():
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "address.postcode" : 1}
    return entries.find({"wheelchair" : "yes"}, projection)

# show all places that are wheelchair friendly
pprint.pprint(list(wheelchair_friendly()))
print "Number of wheelchair friendly places:",entries.find({"wheelchair" : "yes"}).count()

def show_toilets():
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "pos" : 1}
    return entries.find({"amenity" : "toilets"}, projection)

pprint.pprint(list(show_toilets()))
print "Number of public toilets:",entries.find({"amenity" : "toilets"}).count()

# Show all the different types of restaurants and count them
pipeline = [{ "$match" : { "cuisine": { "$exists": 1}}},
    { "$group": { "_id": "$cuisine", "count": { "$sum" : 1} } },
    { "$sort": { "count": -1 } }]

pprint.pprint(list(entries.aggregate(pipeline)))

# Sort postcodes by count     
pipeline = [{ "$match":{"address.postcode":{"$exists":1}}}, 
    {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, 
    {"$sort":{"count": -1}}]

pprint.pprint(list(entries.aggregate(pipeline)))

# Sort cities by count, descending
pipeline = [{"$match":{"address.city":{"$exists":1}}}, 
    {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, 
    {"$sort":{"count":-1}}]

pprint.pprint(list(entries.aggregate(pipeline)))