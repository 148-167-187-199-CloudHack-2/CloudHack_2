import pika
import os
import time

# set these via the Dockerfile
SERVER_IP = os.environ["SERVER_IP"]
SERVER_PORT = os.environ["SERVER_PORT"]
CUST_ID= os.environ["CUST_ID"]

def get_time_from_rabbit(ch, method, properties, body):
	val_passed = body.decode()
	time_to_sleep = int(val_passed)
	print("Sleeping for %r seconds", time_to_sleep)
	time.sleep(time_to_sleep) 

if __name__ == '__main__':
	connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel=connection.channel()
	channel.queue_declare(queue='new_ride_queue')
	channel.basic_consume(queue='new_ride_queue', on_message_callback=get_time_from_rabbit, auto_ack=True)
	channel.start_consuming()
