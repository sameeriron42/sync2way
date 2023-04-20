from fastapi import HTTPException,Request
from sqlalchemy.orm import Session
from routers import models
from dotenv import load_dotenv
from services import customer_handler
import stripe
import customer_handler
import os
import stripe


load_dotenv()
stripe.api_key = os.getenv("STRIPE_RESTRICTED_KEY")
endpoint_secret = os.getenv("WEBHOOK_SECRET")

async def stripeWebhook(request: Request,db_instance:Session):
    event = None
    payload = await request.body()
    sig_header = request.headers.get('STRIPE-SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HTTPException(403,detail=e)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HTTPException(403,detail=e)

    # Handle the event
    if event['type'] == 'customer.created':
      stripe_customer = event['data']['object']
      customer = models.Customer(name=stripe_customer["name"],email=stripe_customer["email"])
      customer_handler.createCustomer(customer,db_instance,webhook=True)

    elif event['type'] == 'customer.deleted':
      stripe_customer = event['data']['object']
      customer_handler.deleteCustomer(stripe_customer["email"],db_instance,webhook=True)

    elif event['type'] == 'customer.updated':
      stripe_customer = event['data']['object']
      customer = models.Customer(name=stripe_customer["name"],email=stripe_customer["email"])
      customer_handler.updateCustomer(stripe_customer["email"],customer,db_instance,webhook=True)
      
    else:
      raise HTTPException(status_code=404,detail=f'Invalid event type: {event["type"]}')   

    
    raise HTTPException(status_code=200,detail=f'success')   


