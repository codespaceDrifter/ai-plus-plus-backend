from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    core: str
    isUser: bool

class Messages(BaseModel):
    messages: List[Message]


memory_db = {"messages": []}