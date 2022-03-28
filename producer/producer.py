from flask import Flask, request, jsonify
import pika

# use pika for RabbitMQ connections

app = Flask(__name__)

@app.route("/new_ride", methods=['POST'])
def handle_new_ride():
	time = request.form['time']

	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
	except pika.exceptions.AMQPConnectionError as exc:
		print("Failed to connect to RabbitMQ service. Message wont be sent.")
		return

	channel=connection.channel() 

	# push time to RabbitMQ client.
	channel.queue_declare(queue='new_ride_queue', durable=True)
	channel.basic_publish(
		exchange='',
		routing_key='new_ride_queue',
		body=time,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
		))

	connection.close()

	return "Sent message" + time + "to receiver"


@app.route("/new_ride_matching_customer", methods=['POST'])
def handle_new_customer():
	customer = jsonify(request.form)

	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
	except pika.exceptions.AMQPConnectionError as exc:
		print("Failed to connect to RabbitMQ service. Message wont be sent.")
		return

	channel=connection.channel() 

	channel.queue_declare(queue='new_ride_matching_queue', durable=True)
	channel.basic_publish(
		exchange='',
		routing_key='new_ride_matching_queue',
		body=time,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
		))

	connection.close()

	return "Sent" + customer + "to database"

app.run(debug=True)
