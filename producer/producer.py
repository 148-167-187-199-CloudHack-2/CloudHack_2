from flask import Flask, request, jsonify
import pika
import time

# use pika for RabbitMQ connections

app = Flask(__name__)

@app.route("/new_ride", methods=['POST'])
def handle_new_ride():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
	except pika.exceptions.AMQPConnectionError as exc:
		print("Failed to connect to RabbitMQ service. Message wont be sent.")

	channel=connection.channel() 
	
	time = request.form['time']

	# push time to RabbitMQ client.
	channel.queue_declare(queue='new_ride_queue')
	channel.basic_publish(
		exchange='',
		routing_key='new_ride_queue',
		body=time,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
		))

	connection.close()

	return "Sent message " + time + " to receiver\n"


@app.route("/new_ride_matching_customer", methods=['POST'])
def handle_new_customer():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
	except pika.exceptions.AMQPConnectionError as exc:
		print("Failed to connect to RabbitMQ service. Message wont be sent.")

	channel=connection.channel() 
	customer = request.form['cid']

	channel.queue_declare(queue='new_ride_matching_queue')
	channel.basic_publish(
		exchange='',
		routing_key='new_ride_matching_queue',
		body=customer,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
		))

	connection.close()

	return "Sent " + customer + " to database"

app.run(host='0.0.0.0', port=5000, debug=True)