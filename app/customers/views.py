from fastapi import APIRouter,Depends,HTTPException,Request
from sqlalchemy.orm import Session
from app.core import schemas 
from app.customers import customer_handler
from app.core.dependency import get_db

router = APIRouter()



@router.get("/customers", response_model=list[schemas.Customer])
async def get_all_customers(db:Session = Depends(get_db)):
    return customer_handler.getAllCustomers(db)

@router.get("/customers/{email}",response_model=schemas.Customer)
async def get_customer_by_email(email,db:Session= Depends(get_db)):
    return customer_handler.getCustomerByEmail(email,db)

@router.post("/customers", response_model=schemas.Customer)
async def create_customer(request:Request,customer : schemas.Customer,db:Session = Depends(get_db)):
    return customer_handler.createCustomer(request,customer,db)

@router.put("/customers/{email}", response_class=HTTPException)
async def update_customer(request:Request,email:str, customer: schemas.Customer, db: Session = Depends(get_db)):
    return await customer_handler.updateCustomer(request,email,customer,db)


@router.delete("/customers/{email}",response_class=HTTPException)
async def delete_customer(request:Request,email:str,db:Session = Depends(get_db)):
    return await customer_handler.deleteCustomer(request,email,db)