#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pprint
import subprocess

filename="lucerne.osm"

from pymongo import MongoClient
db_name = "osm"

client = MongoClient('localhost:27017')
db = client[db_name]

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

volusia_flagler = db[collection]

print "db[collection]", db[collection]
print "volusia_flagler", volusia_flagler
print "volusia_flagler.find().count()", volusia_flagler.find().count()
print "volusia_flagler.find()", volusia_flagler.find()
print len(volusia_flagler.distinct('created.user'))


pipeline = [{"$group": { "_id": "$created.user", "count": { "$sum" : 1} } },
	{ "$sort": { "count": -1 } },
	{"$limit" : 10}]

most_active_user = db.lucerne.aggregate(pipeline)
print list(most_active_user)


'''volusia_flagler.aggregate([{"$group" : {"_id" : "$created.user", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}, \
                           {"$limit" : 1}])['result']

print volusia_flagler.aggregate({"$group" : {"_id" : "$type", "count" : {"$sum" : 1}}})['result']

node_id = volusia_flagler.aggregate([{"$unwind" : "$node_refs"}, \
                                     {"$group" : {"_id" : "$node_refs", "count" : {"$sum" : 1}}}, \
                                     {"$sort" : {"count" : -1}}, \
                                     {"$limit" : 1}])['result'][0]['_id']

pprint.pprint(volusia_flagler.find({"id" : node_id})[0])

volusia_flagler.find({"address.street" : {"$exists" : 1}}).count()

volusia_flagler.aggregate([{"$match" : {"address.postcode" : {"$exists" : 1}}}, \
                           {"$group" : {"_id" : "$address.postcode", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}])['result']

volusia_flagler.aggregate([{"$match" : {"address.city" : {"$exists" : 1}}}, \
                           {"$group" : {"_id" : "$address.city", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}, \
                           {"$limit" : 5}])['result']

volusia_flagler.aggregate([{"$match" : {"amenity" : {"$exists" : 1}}}, \
                           {"$group" : {"_id" : "$amenity", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}, \
                           {"$limit" : 10}])['result']

religions = volusia_flagler.aggregate([{"$match" : {"amenity" : "place_of_worship"}}, \
                           {"$group" : {"_id" : {"religion" : "$religion", "denomination" : "$denomination"}, "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}])['result']

pprint.pprint(religions)

volusia_flagler.aggregate([{"$match" : {"leisure" : {"$exists" : 1}}}, \
                           {"$group" : {"_id" : "$leisure", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"count" : -1}}, \
                           {"$limit" : 10}])['result']

volusia_flagler.aggregate([{"$project" : {"dayOfWeek" : {"$dayOfWeek" : "$created.timestamp"}}}, \
                           {"$group" : {"_id" : "$dayOfWeek", "count" : {"$sum" : 1}}}, \
                           {"$sort" : {"_id" : 1}}])['result']
'''

entries = db.lucerne

def find():
    
    projection = {"_id" : 0, "address.street" : 1}
        
    streets = entries.find({"address.street" : {"$exists": 1}}, projection)
    
    print "number of entries without street name: ",entries.find({"address.street" : {"$exists": 0}}, projection).count()
    print "number of entries with street name: ",entries.find({"address.street" : {"$exists": 1}}, projection).count()
    print "number of entries with street name that contains 'Strasse': ",entries.find({"address.street" : {"$exists": 1},"address.street" : {"$regex": "[Ss]trasse"}}, projection).count()
    
    expected = ["strasse","Strasse", "platz", "weg","gasse","str.","matt","matte","halde", "quai", "ring", "hof", "weid"]
    
    for e in expected:
        numOfCounts = entries.find({"address.street" : {"$exists": 1},"address.street" : {"$regex": e}}, projection).count()
        print "number of entries with street name that contains ", e,": ", numOfCount

def find_restaurant_by_postcode(postcode):
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "address.postcode" : 1}
    return entries.find({ "$and": [ {"address.postcode" : {"$eq" : str(postcode)}},
                                   {"amenity": {"$eq" : "restaurant"}},
                                 {"name": {"$exists": 1}},
                                 {"address.street": {"$exists": 1}} ] }, projection)

# find a restaurant in my hometown
pprint.pprint(list(find_restaurant_by_postcode(6006)))

# Print out the 10 most active user
pipeline = [{"$group": { "_id": "$created.user", "count": { "$sum" : 1} } },
	{ "$sort": { "count": -1 } },
	{"$limit" : 10}]

most_active_user = entries.aggregate(pipeline)
list(most_active_user)


def wheelchair_friendly():
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "address.postcode" : 1}
    return entries.find({"wheelchair" : "yes"}, projection)

# show all places that are wheelchair friendly
print entries.find({"wheelchair" : "yes"}).count()
pprint.pprint(list(wheelchair_friendly()))

def show_toilets():
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "pos" : 1}
    return entries.find({"amenity" : "toilets"}, projection)

# show all toilets with coordinates
print entries.find({"amenity" : "toilets"}).count()
pprint.pprint(list(show_toilets()))

# Show all the different types of restaurants and count them
pipeline = [{ "$match" : { "cuisine": { "$exists": 1}}},
    { "$group": { "_id": "$cuisine", "count": { "$sum" : 1} } },
    { "$sort": { "count": -1 } }]

count_restaurants = entries.aggregate(pipeline)
list(count_restaurants)

# Sort postcodes by count     
pipeline = [{ "$match":{"address.postcode":{"$exists":1}}}, 
    {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, 
    {"$sort":{"count": -1}}]

postcodes=entries.aggregate(pipeline)
list(postcodes)

# Sort cities by count, descending
pipeline = [{"$match":{"address.city":{"$exists":1}}}, 
    {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, 
    {"$sort":{"count":-1}}]

cities_count = entries.aggregate(pipeline)
list(cities_count)