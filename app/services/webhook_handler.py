from fastapi import HTTPException,Request
from sqlalchemy.orm import Session
from routers import models
from dotenv import load_dotenv
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
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        raise e

    # Handle the event
    if event['type'] == 'customer.created':
      stripe_customer = event['data']['object']
      customer = models.Customer(name=stripe_customer["name"],email=stripe_customer["email"])
      await customer_handler.createCustomer(customer=customer,db=db_instance,webhook=True)

    elif event['type'] == 'customer.deleted':
      stripe_customer = event['data']['object']
      await customer_handler.deleteCustomer(stripe_customer["email"],db=db_instance,webhook=True)

    elif event['type'] == 'customer.updated':
      stripe_customer = event['data']['object']
      customer = models.Customer(name=stripe_customer["name"],email=stripe_customer["email"])
      await customer_handler.updateCustomer(email=stripe_customer["email"],customer=customer,db=db_instance,webhook=True)
      
    else:
      raise HTTPException(status_code=404,detail=f'Invalid event type: {event["type"]}')   

    return 200

