import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Message(BaseModel):
    message: str

class Messages(BaseModel):
    messages: List[Message]

origins = [
    "http://localhost:5173",
    "http://ai-plus-plus.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"messages": []}

@app.get("/messages", response_model=Message)
def get_messages():
    return Message(message="Default message")

@app.post("/messages", response_model=Message)
def post_message(message: Message):
    memory_db["messages"].append(message)
    return message

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
