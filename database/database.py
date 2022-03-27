#!/usr/bin/env python
import pika, sys, os
import random
import tqdm
import pymongo
from pymongo import MongoClient
from flask import jsonify
import json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='new_ride_matching_queue')

    def callback(ch, method, properties, body):
        val_passed= body.decode()
        obj = json.loads(val_passed) 

        #code to add data into mongo db
        CONN_STR = "mongodb+srv://gayathri-sunil:NySZ8OCAEE1uQZap@cluster0.mn5ub.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = MongoClient(CONN_STR)

        db = client["ride-share-db"]
        collection = db["ride-share"]
        cust_id = random.randint(100000,999999)
        obj["cust_id"]= cust_id
        collection.insert_one(obj)

        print("Inserted into database successfully")

    channel.basic_consume(queue='new_ride_matching_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)