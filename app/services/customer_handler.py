from fastapi import HTTPException
from sqlalchemy.orm import Session
from routers import models 
from databases import db_utils
from queues.producer import publish_to_queue


def getAllCustomers(db_instance:Session):
    customer_list:list[models.Customer] = db_utils.get_users(db_instance)
    if customer_list==[]:
        raise HTTPException(404,detail="No entries yet")

    return customer_list

def getCustomerByEmail(email: str, db_instance: Session):
    customer = db_utils.get_user_by_email(db_instance,email)
    if customer ==None:
        raise HTTPException(status_code=404,detail=f"User with {email} email does not exist")
    return customer

def createCustomer(customer : models.Customer, db_instance:Session, webhook:bool=False):
    db_customer = db_utils.get_user_by_email(db_instance, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    record = db_utils.create_user(db=db_instance,customer=customer)
    record = models.Customer.from_orm(record)
    msg = {"type": "create", "data": record.dict()}
    if webhook==False:
        publish_to_queue(msg)
    return record

def updateCustomer(email:str,customer:models.Customer,db_instance:Session,webhook:bool=False):
    db_customer = db_utils.get_user_by_email(db_instance, email=email)
    if db_customer==None:
        raise HTTPException(status_code=400, detail="Customer with Email does not exist")

    no_of_records = db_utils.update_user(db=db_instance,email=email,customer=customer)
    msg = {"type": "update", "data": customer.dict(),"email": email}
    if webhook==False:
        publish_to_queue(msg)
    raise HTTPException(status_code=200,detail=f'updated {no_of_records} records successfully')

def deleteCustomer(email:str,db_instance:Session,webhook:bool=False):
    db_customer = db_utils.get_user_by_email(db_instance, email=email)
    if db_customer==None:
        raise HTTPException(status_code=400, detail="No Deletion,Customer with Email does not exist")
    no_of_records = db_utils.delete_user(db_instance,email)
    msg = {"type": "delete","email": email}
    if webhook==False:
        publish_to_queue(msg)
    raise HTTPException(status_code=200,detail=f'Deleted {no_of_records} records successfully')
 