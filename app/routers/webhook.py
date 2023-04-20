from fastapi import APIRouter,FastAPI,HTTPException,Request,Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os,sys
import stripe
import routers.customers as customer_router
from routers import models,dependency

load_dotenv()
stripe.api_key = os.getenv("STRIPE_RESTRICTED_KEY")
endpoint_secret = os.getenv("WEBHOOK_SECRET")

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(dependency.get_db)):
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
      await customer_router.createCustomer(customer=customer,db=db,origin='webhook')

    elif event['type'] == 'customer.deleted':
      stripe_customer = event['data']['object']
      await customer_router.deleteCustomer(stripe_customer["email"],db=db,origin='webhook')
    elif event['type'] == 'customer.updated':
      stripe_customer = event['data']['object']
      customer = models.Customer(name=stripe_customer["name"],email=stripe_customer["email"])
      await customer_router.updateCustomer(email=stripe_customer["email"],customer=customer,db=db,origin='webhook')

    raise HTTPException(status_code=200,detail=f' success')