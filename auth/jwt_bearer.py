# Code copied from github.com/overrideveloper/HowAreYouApi*

from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from helper.helpers import user_helper
from models.Database import Database
from models.model import TokenPayload
from auth.encode_decode import decodeJWT, validateJWT
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
            users: Dict[str, dict] = self.db.retrieve(user_helper) or {}
            # TODO: Fix the retrieval from database -> direct connections to the database should be avoided.
            if self.db.get(ObjectId(payload['user_id'])):
                isTokenValid = True

        return isTokenValid