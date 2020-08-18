# Code copied from github.com/overrideveloper/HowAreYouApi*

from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from helper.helpers import user_helper
from models.Database import Database
from models.model import TokenPayload
from auth.encode_decode import decodeJWT
from datetime import time, date
from typing import Dict
import time

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
                raise HTTPException(status_code=409, detail="You are not authorized to access this resource")

            if not self.verify_jwt(credentials.credentials):
                print("Failed here two")
                raise HTTPException(status_code=401, detail="You are not authorized to access this resource")

            return credentials.credentials
        else:
            print("Failed here three")
            raise HTTPException(status_code=401, detail="You are not authorized to access this resource")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload: TokenPayload = None
        isTokenValid: bool = False

        try:
            payload = TokenPayload(**decodeJWT(jwtoken))
        except:
            payload = None

        if payload:
            if time.mktime(date.today().timetuple()) >= payload.expires:
                pass
            else:
                users: Dict[str, dict] = self.db.retrieve(user_helper) or {}

            # I don't know if this is sane - should I be connecting to the database directly?
            # Doesn't it defeat the purpose of the `users` variable above?

            if self.db.get(ObjectId(payload.user_id)):
                isTokenValid = True

        return isTokenValid