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

	ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
	time.sleep(60)

	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
		channel=connection.channel()
	
		channel.queue_declare(queue='new_ride_queue')

		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(queue='new_ride_queue', on_message_callback=get_time_from_rabbit, auto_ack=True)
		channel.start_consuming()
	
	except pika.exceptions.AMQPConnectionError as exc:
		print("Failed to connect to RabbitMQ service. Message wont be sent.")
