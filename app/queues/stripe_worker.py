import pika
import stripe
from dotenv import load_dotenv
import os
import json


load_dotenv()
stripe.api_key = os.getenv('STRIPE_RESTRICTED_KEY')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare('tst')

def handleMsg(ch,method,props,body:bytes):
    body = json.loads(body.decode())
    print(body)
    try:
        stripe.Customer.create(name=body["name"],email=body["email"],metadata={"id":body["id"]})
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except stripe.error.InvalidRequestError as e:
        print(f"Invalid Request Parameter: {e.param}")
    except Exception as e:
        print(f"an error occured: {e}")


channel.basic_consume(queue='tst',on_message_callback= handleMsg)
print('starting to consume...')
channel.start_consuming()
