from fastapi import APIRouter
from app.messageHander import Message, Messages
from dependencies import client
from app.messageHander import get_message_handler, post_message_handler
from pydantic import BaseModel

class MessageRequest(BaseModel):
  core: str

router = APIRouter()

@router.get("/messages")
async def get_message():
  return get_message_handler()

@router.post("/messages")
async def post_message(message: MessageRequest):
  print("Received POST request with message:", message.core)
  return post_message_handler(message.core)


