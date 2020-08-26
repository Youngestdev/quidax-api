import time

import jwt
from decouple import config

from helper.responses import token_response

JWT_SECRET = config('secret')


def signJWT(user_id: str) -> str:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 240
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode())


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return None
