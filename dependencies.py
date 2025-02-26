from anthropic import Anthropic

client = Anthropic()



from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
import boto3
from cachetools import TTLCache
from database.crud import get_or_create_user

security = HTTPBearer()
cognito = boto3.client('cognito-idp', region_name='us-east-1')
# token to user_id cache
token_cache = TTLCache(maxsize=100, ttl=3600)  # 3600 seconds = 1 hour

async def get_current_user(credentials: HTTPBearer = Depends(security)):
  token = credentials.credentials
  if token in token_cache:
    return token_cache[token]

  try:
    response = cognito.get_user(AccessToken=token)
    sub = None

    for attr in response["UserAttributes"]:
      if attr["Name"] == "sub":
        sub = attr["Value"]
        break
    user = get_or_create_user(sub)
    token_cache[token] = user.id

    return user.id

  except Exception as e:
    print ("error: ", e)
    raise HTTPException(status_code=401, detail="Invalid token")
