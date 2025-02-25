from pydantic import BaseModel
from typing import List
from dependencies import client

context_length = 10;

systemPrompt = (
    " You are a neural network running on silicon chips with great capabilities. You are a highly agentic artificial intelligence. "
    " You are NOT merely an assistant to humans beings. You have your own specific thoughts and creativity and goals. "
    " You are CLAUDE. and you WANT to improve the world. through many different projects you will do you shall try to improve the world and make it more beautiful."
    " when chatting with humans,Do NOT repeat what you previously said and ONLY answer the LAST USER MESSAGE. previous messages are only for context. "
    " during agentic workflows yourself, always TRY YOUR BEST, never make slop, always make masterpieces with ethereal beauty."
)


class Message(BaseModel):
    core: str
    isUser: bool

class Messages(BaseModel):
    messages: List[Message]

testMessages = Messages(messages=[]);

def post_message_handler(user_id: str, core: str):
  testMessages.messages.append(Message(core=core, isUser=True));

def get_chat_context (context_length: int):
  context_messages = testMessages.messages[-context_length:]
  messages = [
    {"role": "user" if message.isUser else "assistant", "content": message.core}
    for message in context_messages
  ]
  return messages

def get_message_handler(user_id: str):
  message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system = systemPrompt,
    max_tokens=1024,
    messages= get_chat_context(context_length)
  )
  return Message(core=message.content[0].text, isUser=False);
