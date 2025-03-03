from .models import User, Chat, Message
from .database import engine
from sqlalchemy.orm import Session
from fastapi import HTTPException
from logger import logger
from dependencies import client


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def get_or_create_user(sub: str):
    with Session(engine) as db:
        user = db.query(User).filter(User.sub == sub).first()
        if not user:
            user = User(sub=sub)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

#only call this in routed functions that got userid from security token
def verify_chat(db: Session, user_id: int, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat.user_id != user_id:
        print("Chat Verification Failed Connection Rejected")
        raise HTTPException(status_code=418, detail="Forbidden")

def create_chat(db: Session, user_id: int):
    logger.info("CREATING CHAT DATABASE")
    chat = Chat(
        user_id = user_id,
        name = "New Chat"
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def read_chats(db: Session, user_id: int):
    chats = db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.id.desc()).all()
    return chats

def update_chat_name(db: Session, chat_id: int, name: str):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat.name == "New Chat":
        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            system="Summarize the essence of the message concisely in 4 words or less, words only no punctuation",
            max_tokens=4,
            messages=[{"role": "user", "content": name}]
        )
        chat.name = response.content[0].text
        db.commit()
        db.refresh(chat)


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

