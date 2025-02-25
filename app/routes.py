from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from dependencies import get_current_user
from app.messagesHandler import get_message_handler, post_message_handler
from pydantic import BaseModel

# Create the security validator
security = HTTPBearer()

class MessageRequest(BaseModel):
    core: str

router = APIRouter()

@router.get("/chats")
async def get_chats(credentials: HTTPBearer = Depends(security)):
    user_id = await get_current_user(credentials)
    return get_chats_handler(user_id)

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: int, credentials: HTTPBearer = Depends(security)):
    user_id = await get_current_user(credentials)
    return get_chat_handler(chat_id, user_id)

@router.post("/chats")
async def create_chat(credentials: HTTPBearer = Depends(security)):
    user_id = await get_current_user(credentials)
    return create_chat_handler(user_id)

@router.get("/messages/{chat_id}")
async def get_message(chat_id: int, credentials: HTTPBearer = Depends(security)):
    user_id = await get_current_user(credentials)
    return get_message_handler(chat_id, user_id)

@router.post("/messages/{chat_id}")
async def post_message(
    chat_id: int,
    message: MessageRequest,
    credentials: HTTPBearer = Depends(security)
):
    user_id = await get_current_user(credentials)
    print ("POST message id: ", user_id)
    return post_message_handler(chat_id, user_id, message.core)

