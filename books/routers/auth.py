from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette import status
from tablemodels.user import User
from database.db import dbDependency
from passlib.context import CryptContext

router = APIRouter()

bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserIn(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field()
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)


@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def createUser(db: dbDependency, userIn: UserIn):
    newUser = User(
        name=userIn.name,
        age=userIn.age,
        email=userIn.email,
        password=bcryptContext.hash(userIn.password)
    )
    db.add(newUser)
    db.commit()
