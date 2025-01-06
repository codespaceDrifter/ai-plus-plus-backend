from fastapi import APIRouter
from app.messageHander import Message, Messages
from dependencies import client
from app.messageHander import get_message_handler, post_message_handler

router = APIRouter()

@router.get("/messages")
def get_message():
  return get_message_handler()

@router.post("/messages")
def post_message(message: Message):
  return post_message_handler(message)


