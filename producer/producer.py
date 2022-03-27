from flask import Flask, request, jsonify
import pika

# use pika for RabbitMQ connections
connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel=connection.channel() 

app = Flask(__name__)

@app.route("/new_ride", methods=['POST'])
def handle_new_ride():
    time = request.form['time']

    # push time to RabbitMQ client.
    channel.queue_declare(queue='new_ride_queue')
    channel.basic_publish(exchange='', routing_key='new_ride_queue', body= time)
    print("Sent message to receiver")

    return ""

@app.route("/new_ride_matching_customer", methods=['POST'])
def handle_new_customer():
    customer = jsonify(request.form)
    channel.queue_declare(queue='new_ride_matching_queue')
    channel.basic_publish(exchange='', routing_key='new_ride', body= customer)
    print("Sent to database")
    
    return ""

channel=connection.close()

app.run(debug=True)
