import pika, sys, os
import random
import time
import pymongo
from pymongo import MongoClient
import json

def main():
    time.sleep(60)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        return
    channel = connection.channel()

    channel.queue_declare(queue='new_ride_matching_queue')

    client = MongoClient('mongodb')
    db= client['ride-db']
    colection = db[ "ride-col" ]
    print('Database created')

    def callback(ch, method, properties, body):
        val_passed = body.decode()
        obj= {"cid": val_passed}
        # print(obj)
        collection.insert_one(obj)
        print("Inserted into database")


    channel.basic_qos(prefetch_count=1)
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