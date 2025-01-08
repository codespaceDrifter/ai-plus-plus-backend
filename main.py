import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from routes.messages import router as messages_router
from anthropic import Anthropic

#certibot generated security key

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://ai-plus-plus.com",
    "https://ai-plus-plus.com",
    "http://www.ai-plus-plus.com",
    "https://www.ai-plus-plus.com",
    "http://api.ai-plus-plus.com",
    "https://api.ai-plus-plus.com",
    "http://ai-plus-plus-balancer-641620202.us-east-1.elb.amazonaws.com",
    "https://ai-plus-plus-balancer-641620202.us-east-1.elb.amazonaws.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(messages_router)

print("Available routes:")
for route in app.routes:
    print(f"asdf{route.methods} {route.path}")

@app.get("/health")
async def health_check():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
