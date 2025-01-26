from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.messageHander import Message, Messages
from dependencies import client, get_current_user
from app.messageHander import get_message_handler, post_message_handler
from pydantic import BaseModel

# Create the security validator
security = HTTPBearer()

class MessageRequest(BaseModel):
    core: str

router = APIRouter()

@router.get("/messages")
async def get_message(credentials: HTTPBearer = Depends(security)):
  user_id = await get_current_user(credentials)
  return get_message_handler(user_id)

@router.post("/messages")
async def post_message(
  message: MessageRequest,
  credentials: HTTPBearer = Depends(security)
):
  user_id = await get_current_user(credentials)
  print ("POST message id: ", user_id)
  return post_message_handler(user_id, message.core)


