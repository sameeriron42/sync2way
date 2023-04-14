from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from databases import schemas 
from routers import models 
from databases import db_utils,sql_engine
from routers.dependency import get_db
from queues.producer import publish_to_queue

schemas.Base.metadata.create_all(bind=sql_engine)
router = APIRouter()

@router.get("/customers", response_model=list[models.Customer])
async def getAllCustomers(db:Session = Depends(get_db)):
    return db_utils.get_users(db=db)

@router.post("/customers", response_model=models.Customer)
async def createCustomer(customer : models.Customer,db:Session = Depends(get_db)):
    db_customer = db_utils.get_user_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    record = db_utils.create_user(db=db,customer=customer)
    record = models.Customer.from_orm(record)
    publish_to_queue(record)
    return record

@router.put("/customers/{email}", response_model=str)
async def updateCustomer(email:str, customer: models.Customer, db: Session = Depends(get_db)):
    db_customer = db_utils.get_user_by_email(db, email=email)
    if db_customer==None:
        raise HTTPException(status_code=400, detail="Customer with Email does not exist")
    db_customer = db_utils.get_user_by_email(db,email=customer.email)

    no_of_records = db_utils.update_user(db=db,email=email,customer=customer)
    raise HTTPException(status_code=200,detail=f'updated {no_of_records} records successfully')


@router.delete("/customers/{email}",response_model=str)
async def deleteCustomer(email:str,db:Session = Depends(get_db)):
    db_customer = db_utils.get_user_by_email(db, email=email)
    if db_customer==None:
        raise HTTPException(status_code=400, detail="No Deletion,Customer with Email does not exist")
    no_of_records = db_utils.delete_user(db,email)
    raise HTTPException(status_code=200,detail=f'Deleted {no_of_records} records successfully')
 
