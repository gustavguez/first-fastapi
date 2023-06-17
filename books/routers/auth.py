from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from tablemodels.user import User
from database.db import dbDependency
from services.auth import hashPassword, findValidUser, createAccessToken
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


class UserIn(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field()
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)


class TokenOut(BaseModel):
    access_token: str
    token_type: str


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def createUser(db: dbDependency, userIn: UserIn):
    newUser = User(
        name=userIn.name,
        age=userIn.age,
        email=userIn.email,
        password=hashPassword(userIn.password)
    )
    db.add(newUser)
    db.commit()


@router.post('/token', status_code=status.HTTP_200_OK, response_model=TokenOut)
async def getToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependency):
    user = findValidUser(formData.username, formData.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    token = createAccessToken(user.email, user.id, timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer'}
