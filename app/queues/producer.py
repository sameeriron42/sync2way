import pika
from routers import models

def publish_to_queue(record: models.Customer):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tst')
    msg= record.json()
    channel.basic_publish(exchange='',
                          routing_key='tst',
                          body=msg,    
                          properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))

    print('msg sent to queue')
    print(msg)
    connection.close()
