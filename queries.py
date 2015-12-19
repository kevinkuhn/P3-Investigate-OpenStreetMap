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
        print "number of entries with street name that contains ", e,": ", numOfCounts
        
find()

def find_restaurant_by_postcode(postcode):
    projection = {"_id" : 0, "amenity" : 1, "name" : 1, "address.street" : 1, "address.postcode" : 1}
    return entries.find({ "$and": [ {"address.postcode" : {"$eq" : str(postcode)}},
                                   {"amenity": {"$eq" : "restaurant"}},
                                 {"name": {"$exists": 1}},
                                 {"address.street": {"$exists": 1}} ] }, projection)

# find a restaurant in my hometown
pprint.pprint(list(find_restaurant_by_postcode(6006)))

# Print out the 10 most active user
pipeline = (
	{"$group": { "_id": "$created.user", "count": { "$sum" : 1} } },
	{ "$sort": { "count": -1 } },
	{"$limit" : 10}])
	)

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
pipeline = (
	{ "$match" : { "cuisine": { "$exists": 1}}},
    { "$group": { "_id": "$cuisine", "count": { "$sum" : 1} } },
    { "$sort": { "count": -1 } })

count_restaurants = entries.aggregate(pipeline)
list(count_restaurants)

# Sort postcodes by count     
pipeline = (
	{"$match":{"address.postcode":{"$exists":1}}}, 
    {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, 
    {"$sort":{"count": -1}})

postcodes=entries.aggregate(pipeline)
list(postcodes)

# Sort cities by count, descending
pipeline = (
	{"$match":{"address.city":{"$exists":1}}}, 
    {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, 
    {"$sort":{"count":-1}})

cities_count = entries.aggregate(pipeline)
list(cities_count)