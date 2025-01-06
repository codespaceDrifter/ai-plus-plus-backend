from fastapi import APIRouter
from app.messageHander import Message, Messages


router = APIRouter()

@router.get("/messages")
def get_messages():
  return Message(core="lets all love claudy!!!", isUser=False)
