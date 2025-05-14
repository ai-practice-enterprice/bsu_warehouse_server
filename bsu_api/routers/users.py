import os
import random

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from prisma.models import Users
from typing import Annotated
import bcrypt

from utils.logger import setup_logger
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])
# ======================== models for API request (NOT for database => see schema.prisma) ======================== #
class UserRequest(BaseModel):
    user_id: int

class NewUserRequest(BaseModel):
    active: bool
    admin_privilege: bool
    user_image_path: str
    user_name: str
    user_password: str

class UpdateUserRequest(BaseModel):
    user_id: int
    admin_privilege: bool
    user_name: str
    user_password: str
    active: bool

# ======================== API endpoints for user data ======================== #
@router.post("/user/all")
async def read_users(
    data: UserRequest
):
    """
    Fetch all users except the current user
    """
    users = await Users.prisma().find_many(
        where={
            "NOT": [
                {
                    "userID" : data.user_id
                }
            ]
        }
    )
    return users


@router.post("/user")
async def create_user(
    data: NewUserRequest
):
    """
    Create a new user
    """
    try:
        password = str(data.user_password).encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        new_user = await Users.prisma().create(
            data={
                "active": data.active,
                "adminPrivilege": data.admin_privilege,
                "userImagePath": "",
                "userName": data.user_name,
                "userPassword": hashed_password.decode(), 
            }
        )
    except Exception as e: 
        log.exception(f"AI Server encountered some error when trying to insert the fetched data {e}")
        raise HTTPException(status_code=500, detail="AI Server encountered some error when trying to insert the fetched data")

    return new_user


@router.post("/user/all/admin")
async def read_admin_users():
    """
    Fetch all admin users
    """
    admin_users = await Users.prisma().find_many(
        where={"adminPrivilege":True}
    )
    return admin_users

@router.post("/user/select")
async def read_a_user(
    data: UserRequest
):
    """
    Fetch a specific user
    """
    users = await Users.prisma().find_many(
        where={
            "userID" : data.user_id
        }
    )
    return users

@router.post("/user/update")
async def change_a_user(
    data: UpdateUserRequest
):
    """
    Update a specific user
    """

    password = str(data.user_password).encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    data_user = {}

    if data.user_password != "":
        data_user["userPassword"] = hashed_password.decode()
    if data.user_name != "":
        data_user["userName"] = data.user_name
    if data.admin_privilege != "":
        data_user["adminPrivilege"] = data.admin_privilege
    if data.active != "":
        data_user["active"] = data.active

    users = await Users.prisma().update(
        where={
            "userID" : data.user_id
        },
        data=data_user
    )
    return users