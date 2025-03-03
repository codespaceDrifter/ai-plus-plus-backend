import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as messages_router
import database
from logger import logger

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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(messages_router)

'''
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    logger.info(f"Response status: {response.status_code}")
    return response
'''

@app.get("/health")
async def health_check():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
