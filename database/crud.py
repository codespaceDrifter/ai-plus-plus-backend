from .models import User, Chat, Message
from .database import engine
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dependencies import token_cache, cognito, security, Depends


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

#only call this in routed functions that got userid from security token
def verify_chat(db: Session, user_id: int, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

def create_chat(db: Session, user_id: int):
    chat = Chat(
        user_id = user_id,
        name = "New Chat"
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def read_chats(db: Session, user_id: int):
    chats = db.query(Chat).filter(Chat.user_id == user_id).all()
    return chats


def create_message(db: Session, chat_id: int, core: str, is_user: bool):
    message = Message(
        chat_id = chat_id,
        core = core,
        is_user = is_user
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def read_messages(db: Session, chat_id: int):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages

def read_last_message(db: Session, chat_id: int):
    message = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.id.desc()).first()
    return message

