#!/usr/bin/env python
import pika, sys, os
import random
import tqdm
import pymongo
from pymongo import MongoClient

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='new_ride_queue')

    def callback(ch, method, properties, body):
        #getting message from the body
        val_passed= body.decode()


        #code to add data into mongo db
        CONN_STR = "mongodb+srv://gayathri-sunil:NySZ8OCAEE1uQZap@cluster0.mn5ub.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = MongoClient(CONN_STR)

        db = client["ride-share-db"]
        collection= db["ride-share"]
        cust_id= random.randint(100000,999999)
        doc= { "custID": cust_id,
        "pickup": str(val_passed.split(' ')[0]),
        "destination": str(val_passed.split(' ')[1]),
        "time": str(val_passed.split(' ')[2]),
        "cost": str(val_passed.split(' ')[3]),
        "seats": str(val_passed.split(' ')[4])}
        collection.insert_one(doc)

        print("Inserted into database successfully")


    channel.basic_consume(queue='new_ride_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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