import pymongo
from pymongo import MongoClient

#usrname= "gayathri-sunil"
#pass="NySZ8OCAEE1uQZap"

CONN_STR = "mongodb+srv://gayathri-sunil:NySZ8OCAEE1uQZap@cluster0.mn5ub.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONN_STR)

db = client["ride-share-db"]
collection= db["ride-share"]

#need to change this later to get it from local host
doc= {  "custID": 28749387,
		"pickup": "mypickuploc",
		"destination": "mydroploc",
		"time": "2022-03-26T11:30:05",
		"cost": 120,
		"seats": 2}
collection.insert_one(doc)

