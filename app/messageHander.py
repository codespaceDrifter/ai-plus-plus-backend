from pydantic import BaseModel
from typing import List
from dependencies import client

context_length = 10;

class Message(BaseModel):
    core: str
    isUser: bool

class Messages(BaseModel):
    messages: List[Message]

testMessages = Messages(messages=[]);

def post_message_handler(core: str):
  testMessages.messages.append(Message(core=core, isUser=True));

def get_chat_context (context_length: int):
  context_messages = testMessages.messages[-context_length:]
  messages = [
      {"role": "user" if message.isUser else "assistant", "content": message.core}
      for message in context_messages
  ]
  return messages

def get_message_handler():
  message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages= get_chat_context(context_length)
  )
  return Message(core=message.content[0].text, isUser=False);

