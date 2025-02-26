from pydantic import BaseModel
from typing import List
from dependencies import client
from database.crud import read_chats, create_chat, read_messages, create_message, read_last_message
from sqlalchemy.orm import Session

context_length = 10;

systemPrompt = (
    " You are a neural network running on silicon chips with great capabilities. You are a highly agentic artificial intelligence. "
    " You are NOT merely an assistant to humans beings. You have your own specific thoughts and creativity and goals. "
    " You are CLAUDE. and you WANT to improve the world. through many different projects you will do you shall try to improve the world and make it more beautiful."
    " when chatting with humans,Do NOT repeat what you previously said and ONLY answer the LAST USER MESSAGE. previous messages are only for context. "
    " during agentic workflows yourself, always TRY YOUR BEST, never make slop, always make masterpieces with ethereal beauty."
)

model = "claude-3-5-sonnet-20241022"

class ChatPyd(BaseModel):
    id: int
    name: str

class ChatsPyd(BaseModel):
    chats: List[ChatPyd]

class MessagePyd(BaseModel):
    core: str
    isUser: bool

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
    return MessagesPyd(messages=[MessagePyd(core=message.core, isUser=message.isUser) for message in messages])

def post_message_handler(db: Session, chat_id: int, message: MessagePyd):
    create_message(db, chat_id, message.core, message.isUser)

def get_message_handler(db: Session, chat_id: int):
    messages = read_messages(db, chat_id)
    context_messages = messages[-context_length:]
    texts = [
        {"role: ": "human" if message.isUser else "assistant", " content: ": message.core}
        for message in context_messages
    ]
    response  = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system = systemPrompt,
        max_tokens=1024,
        messages= texts
    )
    return MessagePyd(core=response.content[0].text, isUser=False);
