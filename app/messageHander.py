from pydantic import BaseModel
from typing import List
from dependencies import client

class Message(BaseModel):
    core: str
    isUser: bool

class Messages(BaseModel):
    messages: List[Message]

testMessages = Messages(messages=[]);


def get_message_handler():
  message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": testMessages.messages[-1].core}
      ]
    )
  return Message(core=message.content[0].text, isUser=False);

def post_message_handler(core: str):
  testMessages.messages.append(Message(core=core, isUser=True));
