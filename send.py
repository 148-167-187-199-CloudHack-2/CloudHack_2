#!/usr/bin/env python
import pika
from datetime import datetime
import sys

message = ''.join(sys.argv[1])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='new_ride_queue')

channel.basic_publish(exchange='', routing_key='new_ride_queue', body=message)
print(" [x] Sent time to receiver")
connection.close()