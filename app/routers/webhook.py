from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from services import webhook_handler
from routers import dependency

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(dependency.get_db)):
  return webhook_handler.stripeWebhook(request,db)