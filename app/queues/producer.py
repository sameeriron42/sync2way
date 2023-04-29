import pika
import json

def publish_to_queue(queue_name:str,msg: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name,durable=True)

    msg_str = json.dumps(msg) 
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=msg_str,    
                          properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))

    print('msg sent to queue')
    print(msg_str)
    connection.close()
