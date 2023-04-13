from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from databases import models as db_models
from routers import models as pydt_models
from databases import db_utils,sql_engine,SessionLocal
from typing import List 

db_models.Base.metadata.create_all(bind=sql_engine)
router = APIRouter()
#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers",response_model=List[pydt_models.Customer])
async def getAllCustomers(db:Session = Depends(get_db)):
    print('hi############################\n\n\n\n')
    return db_utils.get_users(db=db)

@router.post("/customers",response_model=pydt_models.Customer)
async def createCustomer(customer : pydt_models.Customer,db:Session = Depends(get_db)):
    return db_utils.create_user(db=db,customer=customer)