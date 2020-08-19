# Code copied from github.com/overrideveloper/HowAreYouApi*

from typing import List

from bson import ObjectId
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.encode_decode import decodeJWT, validateJWT
from models.Database import Database
from models.model import TokenPayload


class JWTBearer(HTTPBearer):
    db: Database = None
    def __init__(self, db, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.db = db

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                print("Failed here.")
                raise HTTPException(status_code=403, detail="Invalid authentication token")

            if not self.verify_jwt(credentials.credentials):
                print("Failed here two")
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return credentials.credentials
        else:
            print("Failed here three")
            raise HTTPException(status_code=403, detail="Invalid authorization token")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload: TokenPayload = None
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if validateJWT(payload):
            users: List = self.db.retrieve()
            user_id = str(ObjectId(payload['user_id']))
            if user_id in users:  # At the moment, this is the best I can do.
                isTokenValid = True
        return isTokenValid