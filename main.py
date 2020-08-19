from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from models.Database import Database
from routes.book import router as BookRouter
from routes.user import router as UserRouter

app = FastAPI()
bearer = JWTBearer(Database())


@app.get("/")
def read_root():
    return {"message": "Welcome to Quidax Book API, use the /docs route,"}


app.include_router(BookRouter, tags=["books"], prefix="/book", dependencies=[Depends(bearer)])
app.include_router(UserRouter, tags=["users"], prefix="/user")
