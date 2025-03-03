from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from dependencies import get_current_user
from database.crud import get_db, verify_chat
from sqlalchemy.orm import Session
from app.messagesHandler import get_chats_handler, create_chat_handler, get_chat_handler, get_message_handler, post_message_handler, MessagePyd
from logger import logger

#TODO: need to change what front end send and receive to postmessage. receive ALL pydantic models and SEND ALL Pydantic models.

# Create the security validator
security = HTTPBearer()

router = APIRouter()

@router.get("/chats")
async def get_chats(credentials: HTTPBearer = Depends(security), db: Session = Depends(get_db)):
    user_id = await get_current_user(credentials)
    return get_chats_handler(db, user_id)

@router.post("/chats")
async def create_chat(credentials: HTTPBearer = Depends(security), db: Session = Depends(get_db)):
    logger.info("CREATING CHAT ROUTE")
    user_id = await get_current_user(credentials)
    return create_chat_handler(db, user_id)

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: int, credentials: HTTPBearer = Depends(security), db: Session = Depends(get_db)):
    user_id = await get_current_user(credentials)
    verify_chat(db, user_id, chat_id)
    return get_chat_handler(db, chat_id)

@router.get("/messages/{chat_id}")
async def get_message(chat_id: int, credentials: HTTPBearer = Depends(security), db: Session = Depends(get_db)):
    user_id = await get_current_user(credentials)
    verify_chat(db, user_id, chat_id)
    return get_message_handler(db, chat_id)

@router.post("/messages/{chat_id}")
async def post_message(chat_id: int, message: MessagePyd, credentials: HTTPBearer = Depends(security), db: Session = Depends(get_db)):
    user_id = await get_current_user(credentials)
    verify_chat(db, user_id, chat_id)
    return post_message_handler(db, chat_id, message)
