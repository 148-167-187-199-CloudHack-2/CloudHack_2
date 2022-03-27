import pika

import os
import time

# set these via the Dockerfile
SERVER_IP = os.environ["SERVER_IP"]
SERVER_PORT = os.environ["SERVER_PORT"]

def on_open(connection):
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(channel):
	# define this using the pika interface.
	pass

def get_time_from_rabbit(connection):
	# Set up RabbitMQ client here with pika.

	# Unsure how to do this. Adding a link that may help:
	## https://github.com/jay-johnson/kombu-and-pika-pub-sub-examples/tree/master/pika

	return time # return an int pls

if __name__ == '__main__':
	connection = pika.SelectConnection(on_open_callback=on_open)

	time = get_time_from_rabbit(connection)
	time.sleep(time)

	# this may need refactoring; the consumers are a continuous looping process.