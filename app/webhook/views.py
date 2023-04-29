from fastapi import APIRouter,Request,Depends,HTTPException
from sqlalchemy.orm import Session
from app.webhook import webhook_handler
from app.core import dependency

router = APIRouter()

@router.post("/webhook",response_class=HTTPException)
async def webhook(request: Request, db: Session = Depends(dependency.get_db)):
  await webhook_handler.stripeWebhook(request,db)