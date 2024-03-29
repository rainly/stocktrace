'''
Created on 2012-10-12

@author: Simon
'''
import pika
from util import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBIT_SERVER))
channel = connection.channel()

channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()