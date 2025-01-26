from anthropic import Anthropic

client = Anthropic()

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
import boto3
from cachetools import TTLCache

security = HTTPBearer()

# Initialize Cognito client
cognito = boto3.client('cognito-idp', region_name='us-east-1')

# Cache for verified tokens - stores in RAM for 1 hour
token_cache = TTLCache(maxsize=100, ttl=3600)  # 3600 seconds = 1 hour

async def get_current_user(credentials: HTTPBearer = Depends(security)):
  token = credentials.credentials

  print ("token: ", token)

  if token in token_cache:
    print ("token in cache", token_cache[token])
    return token_cache[token]

  try:
    # Verify token with Cognito
    response = cognito.get_user(AccessToken=token)
    user_id = None
    for attr in response["UserAttributes"]:
      if attr["Name"] == "sub":
        user_id = attr["Value"]
        break
 
    token_cache[token] = user_id  # Cache just the string


    print ("user_id: ", user_id)
    return user_id

  except Exception as e:
    print ("error: ", e)
    raise HTTPException(status_code=401, detail="Invalid token")