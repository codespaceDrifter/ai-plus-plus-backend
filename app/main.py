import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://ai-plus-plus.com",
    "https://ai-plus-plus.com",
    "http://www.ai-plus-plus.com",
    "https://www.ai-plus-plus.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    core: str
    isUser: bool

class Messages(BaseModel):
    messages: List[Message]


memory_db = {"messages": []}

@app.get("/messages", response_model=Message)
def get_messages():
    return Message(core="Default message")

@app.post("/messages", response_model=Message)
def post_message(core: str):
    memory_db["messages"].append(Message(core=core))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
