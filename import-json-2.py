import os


import signal
import subprocess

filename="source/lucerne.osm"

#print "The downloaded file is {} MB".format(os.path.getsize(filename)/1.0e6) # convert from bytes to megabytes


# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
#pro = subprocess.Popen("mongod", preexec_fn = os.setsid) 

from pymongo import MongoClient
db_name = "osm"

client = MongoClient('localhost:27017')
db = client[db_name]

# Build mongoimport command
collection = filename[:filename.find(".")]
working_directory = ""
json_file = filename + ".json"

'''
mongoimport_cmd = "mongoimport --db " + db_name + \
                  " --collection " + collection + \
                  " --file " + working_directory + json_file

# Before importing, drop collection if it exists
if collection in db.collection_names():
    print "dropping collection"
    db[collection].drop()'''

# Execute the command
#print "Executing: " + mongoimport_cmd
#subprocess.call(mongoimport_cmd.split())

volusia_flagler = db[collection]

print volusia_flagler.find().count()
print volusia_flagler.find()

print len(volusia_flagler.distinct('created.user'))

print volusia_flagler.aggregate([{"$group" : {"_id" : "$created.user", "count" : {"$sum" : 1}}}, \
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

