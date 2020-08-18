import jwt
import time
from decouple import config
from fastapi import HTTPException
from models.model import TokenPayload
from datetime import date

JWT_SECRET = config('secret')

def encodeJWT(user_id: str) -> str:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 60
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decodeJWT(token: str) -> dict:
    try:
        jwtoken = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return jwtoken
    except:
        return None

# Validate the JWT token passed.

def validateJWT(token: str):
    if token:
        token = TokenPayload(**token)
        if time.mktime(date.today().timetuple()) >= token.expires:
            raise HTTPException(status_code=401, detail="Expired token, please get another token")
        return True
    return False