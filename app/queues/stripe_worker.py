import pika
import stripe
from dotenv import load_dotenv
import os
import json
import pickle

def createNewCustomer(ch,method,body: dict):
    try:
        response = stripe.Customer.create(name=body["name"],email=body["email"],metadata={"id":body["id"]})
        customer_id = response['id']

        fp = open("../shared.pkl","rb+")
        customer_list = pickle.load(fp)
        customer_list.append(customer_id)
        fp.seek(0)
        pickle.dump(customer_list,fp)
        fp.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Created new stripe customer")
    except stripe.error.InvalidRequestError as e:
        print(f"Invalid Request Parameter: {e.param}")
    except Exception as e:
        print(f"an error occured: {e}")

def updateCustomer(ch,method,body: dict):
    email = body["email"]
    try:
        # response=stripe.Customer.search(query=f"email:'{email}'")
        # if response['data']==[]:
        #     print(f"Stripe does not have customer with email {email}")
        #     return
    
        # customer_id = response['data'][0]["id"]
        response = stripe.Customer.list(email=email)
        customer_id = response['data'][0]['id']

        fp = open("../shared.pkl","rb+")
        customer_list = pickle.load(fp)
        customer_list.append(customer_id)
        fp.seek(0)
        pickle.dump(customer_list,fp)
        fp.close()

        new_data = body["data"]
        stripe.Customer.modify(customer_id,name=new_data['name'])
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Updated Stripe Customer with email {email}")
    except stripe.error.InvalidRequestError as e:
        print(f"Invalid Request Parameter: {e}")
    except Exception as e:
        print(f"an error occured: {e}")

def deleteCustomer(ch,method,body:dict):
    email = body["email"]
    # response=stripe.Customer.search(query=f"email:'{email}'")
    # if response['data']==[]:
    #     print(f"Stripe does not have customer with email {email}")
    #     return
    
    # customer_id = response['data'][0]["id"]
    response = stripe.Customer.list(email=email)
    customer_id = response['data'][0]['id']
    
    fp = open("../shared.pkl","rb+")
    customer_list = pickle.load(fp)
    customer_list.append(customer_id)
    fp.seek(0)
    pickle.dump(customer_list,fp)
    fp.close()

    try:
        stripe.Customer.delete(customer_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Deleted Stripe Customer with email {email}")
    except stripe.error.InvalidRequestError as e:
        print(f"Invalid Request Parameter: {e.param}")
    except Exception as e:
        print(f"an error occured: {e}")


def handleMsg(ch,method,props,body:bytes):
    body = json.loads(body.decode())
    print(body)
    type = body["type"]
    if type=="create":
        customer_data=body["data"]
        createNewCustomer(ch,method,customer_data)
    elif type=="update":
        updateCustomer(ch,method,body)
    elif type=="delete":
        deleteCustomer(ch,method,body)
    else:
        print(f"invalid type {type}")
    

load_dotenv()
stripe.api_key = os.getenv('STRIPE_RESTRICTED_KEY')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare('test',durable=True)

customer_list = []
fp = open("../shared.pkl","wb+")
pickle.dump(customer_list,fp)
fp.close()

channel.basic_consume(queue='test',on_message_callback= handleMsg)
print('starting to consume...')
channel.start_consuming()
