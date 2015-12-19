#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pymongo
from json import JSONDecoder
from functools import partial
import jsonpickle

data = []

def get_db():
    # start MongoClient
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'maps' here is the database name. It will be created if it does not exist.
    db = client.cities
    return db

def add_data(db, data):
    db.cities.insert_one(data)

def load_json(filepath):
    data = open(filepath) #opens the json file and saves the raw contents
    liste = []
    for item in data:
        
        liste.append(item)
        pickled = jsonpickle.encode(item)
    return liste
    #jsonData = json.dumps(pickled) #converts to a json structure
    #return jsonData


if __name__ == "__main__":

    # start mongodb service and create db
    db = get_db()
    print db
    # clean up the whole db
    print "########### DATABASE CLEANOUT ###########"
    print "before", db.cities.count() 
    #db.cities.drop()
    print "after", db.cities.count()
    print "########### END OF CLEANOUT ###########"
    # import json file
    #load_json('source/lucerne.osm.json')
    #add_data(db, load_json('source/lucerne-test.osm.json'))
    #print data
            #data =  json.load(line)
            #data.append(json.loads(line))
            #print data
        # show first entry
    print db.cities.find_one()
        # show collections
    print db.collection_names(include_system_collections=False)
        #number of data set entries
    print db.cities.count()

        # show first entry
    print db.cities.lucerne.find_one()
        # show collections
    print db.collection_names(include_system_collections=False)
        #number of data set entries
    print db.cities.lucerne.count()

        #print db
    # Print out the 10 most active user
    most_active_user = db.cities.aggregate([
            { "$group": { "_id": "$created.user", "count": { "$sum" : 1} } },
            { "$sort": { "count": -1 } },
            {"$limit" : 10}])

    list(most_active_user)