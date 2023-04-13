from fastapi import APIRouter
from routers.models import Customer 
from sqlalchemy import select 
router = APIRouter()

@router.get("/customers")
async def getAllCustomers():
    return {"status":"up"}

@router.post("/customers")
async def createCustomer(json_data: Customer):
    return {"name": json_data.name}