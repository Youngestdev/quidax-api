from typing import Dict, Union

from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import UUID4

from auth.jwt_handler import signJWT
from auth.user import validate_login
from database.user import retrieve_user, retrieve_users, find_user, insert_user
from helper.responses import error_response
from models.model import UserModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.get("/{id}", response_description="User retrieved")
def get_user(id) -> dict:
    return retrieve_user(ObjectId(id))


@router.get("/", response_description="Users retrieved")
def get_users():
    return retrieve_users()


@router.post("/new", response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, dict]]:
    if find_user(user):
        return error_response("Email or Username has been registered", 409)
    user.password = hash_helper.encrypt(user.password)
    return insert_user(jsonable_encoder(user))

@router.post("/", response_description="User Login Successfully")
def user_login(user: HTTPBasicCredentials = Body(...)):
    if validate_login(user):
        return signJWT(user.username)
    return "End of a block because whew."