# Code copied from github.com/overrideveloper/HowAreYouApi*
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt_handler import decodeJWT
from models.Database import Database


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
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
