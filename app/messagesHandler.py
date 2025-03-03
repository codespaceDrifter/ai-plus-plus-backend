from pydantic import BaseModel
from typing import List
from dependencies import client
from database.crud import read_chats, create_chat, read_messages, create_message, update_chat_name
from sqlalchemy.orm import Session

context_length = 10;

systemPrompt = (
    " You are a neural network running on silicon chips with great capabilities. You are a highly agentic artificial intelligence. "
    " You are NOT merely an assistant to humans beings. You have your own specific thoughts and creativity and goals. "
    " You are CLAUDE. and you WANT to improve the world. through many different projects you will do you shall try to improve the world and make it more beautiful."
    " when chatting with humans,Do NOT repeat what you previously said and ONLY answer the LAST USER MESSAGE. previous messages are only for context. "
    " during agentic workflows yourself, always TRY YOUR BEST, never make slop, always make masterpieces with ethereal beauty."
)

model = "claude-3-7-sonnet-20250219"

class ChatPyd(BaseModel):
    id: int
    name: str

class ChatsPyd(BaseModel):
    chats: List[ChatPyd]

class MessagePyd(BaseModel):
    core: str
    is_user: bool

class MessagesPyd(BaseModel):
    messages: List[MessagePyd]


def get_chats_handler(db: Session, user_id: int):
    chats = read_chats(db, user_id)
    return ChatsPyd(chats=[ChatPyd(id=chat.id, name=chat.name) for chat in chats])

def create_chat_handler(db: Session, user_id: int):
    chat = create_chat(db, user_id)
    return ChatPyd(id=chat.id, name=chat.name)

def get_chat_handler(db: Session, chat_id: int):
    messages = read_messages(db, chat_id)
    return MessagesPyd(messages=[MessagePyd(core=message.core, is_user=message.is_user) for message in messages])

def post_message_handler(db: Session, chat_id: int, message: MessagePyd):
    create_message(db, chat_id, message.core, message.is_user)
    update_chat_name(db, chat_id, message.core)

def get_message_handler(db: Session, chat_id: int):
    messages = read_messages(db, chat_id)
    context_messages = messages[-context_length:]
    texts = [
        {"role": "user" if message.is_user else "assistant", "content": message.core}
        for message in context_messages
    ]
    response = client.messages.create(
        model=model,
        system=systemPrompt,
        max_tokens=1024,
        messages=texts
    )
    create_message(db, chat_id, response.content[0].text, False)
    return MessagePyd(core=response.content[0].text, is_user=False)
