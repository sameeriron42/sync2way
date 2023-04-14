import pika
import json
from routers import models

def publish_to_queue(record: models.Customer):
    print("at publish")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tst')
    print("before dict")
    msg= record.json()
    print(f"after dict {msg}")
    channel.basic_publish(exchange='',routing_key='tst',body=msg)
    print('msg sent')
    connection.close()