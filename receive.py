#!/usr/bin/env python
import pika, sys, os
import time
import tqdm


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='new_ride_queue')

    def callback(ch, method, properties, body):
        val_passed= body.decode()
        time_to_sleep= int(val_passed.split(' ')[2])
        print("Microservice sleeping for %r seconds" % time_to_sleep)
        time.sleep(time_to_sleep)
        #for i in tqdm.tqdm(range(time_to_sleep)):
            #time.sleep(0.01)
        print()
        print("Pickup location: ", val_passed.split(' ')[0])
        print("Drop location: ", val_passed.split(' ')[1])
        print("Cost: ", val_passed.split(' ')[3])
        print(": ", val_passed.split(' ')[4])

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
