from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from databases import schemas 
from routers import models 
from databases import db_utils,sql_engine
from routers.dependency import get_db


schemas.Base.metadata.create_all(bind=sql_engine)
router = APIRouter()

@router.get("/customers", response_model=list[models.Customer])
async def getAllCustomers(db:Session = Depends(get_db)):
    return db_utils.get_users(db=db)

@router.post("/customers", response_model=models.Customer)
async def createCustomer(customer : models.Customer,db:Session = Depends(get_db)):
    return db_utils.create_user(db=db,customer=customer)