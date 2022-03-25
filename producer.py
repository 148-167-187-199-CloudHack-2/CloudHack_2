from flask import Flask, request, jsonify

import pika
# use pika for RabbitMQ connections

app = Flask(__name__)

@app.route("/new_ride", methods=['POST'])
def handle_new_ride():
    time = request.form['time']

    # push time to RabbitMQ client.

    return ""

@app.route("/new_ride_matching_customer", methods=['POST'])
def handle_new_customer():
    customer = jsonify(request.form)

    # Send data to RabbitMQ client for specified database topic.

    return ""

app.run(debug=True)
