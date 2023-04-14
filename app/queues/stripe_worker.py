import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare('tst')

def handleMsg(ch,method,props,body):
    print(body.decode())

channel.basic_consume(queue='tst',on_message_callback= handleMsg,auto_ack=True)
print('starting to consume...')
channel.start_consuming()
