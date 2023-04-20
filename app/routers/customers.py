from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from databases import schemas 
from routers import models 
from services import customer_handler
from databases import sql_engine
from routers.dependency import get_db

schemas.Base.metadata.create_all(bind=sql_engine)
router = APIRouter()



@router.get("/customers", response_model=list[models.Customer])
async def get_all_customers(db:Session = Depends(get_db)):
    return customer_handler.getAllCustomers(db)

@router.get("/customers/{email}",response_model=models.Customer)
async def get_customer_by_email(email,db:Session= Depends(get_db)):
    return customer_handler.getCustomerByEmail(email,db)

@router.post("/customers", response_model=models.Customer)
async def create_customer(customer : models.Customer,db:Session = Depends(get_db)):
    return customer_handler.createCustomer(customer,db)

@router.put("/customers/{email}", response_class=HTTPException)
async def update_customer(email:str, customer: models.Customer, db: Session = Depends(get_db)):
    return await customer_handler.updateCustomer(email,customer,db)


@router.delete("/customers/{email}",response_class=HTTPException)
async def delete_customer(email:str,db:Session = Depends(get_db)):
    return await customer_handler.deleteCustomer(email,db)