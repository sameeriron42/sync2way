import pika
import json

def publish_to_queue(msg: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='test',durable=True)
    
    msg_str = json.dumps(msg) 
    channel.basic_publish(exchange='',
                          routing_key='test',
                          body=msg_str,    
                          properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))

    print('msg sent to queue')
    print(msg_str)
    connection.close()
