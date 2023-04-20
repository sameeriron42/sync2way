from fastapi import APIRouter,Request,Depends,HTTPException
from sqlalchemy.orm import Session
from services import webhook_handler
from routers import dependency

router = APIRouter()

@router.post("/webhook",response_class=HTTPException)
async def webhook(request: Request, db: Session = Depends(dependency.get_db)):
  await webhook_handler.stripeWebhook(request,db)