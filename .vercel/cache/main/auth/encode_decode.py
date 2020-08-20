import jwt
from decouple import config

JWT_SECRET = config('secret')

def encodeJWT(payload: dict) -> str:
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decodeJWT(token: str) -> dict:
    try:
        return jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
    except:
        return None
